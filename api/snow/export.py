import logging
import time
import uuid

from flask import request

from snow import constants as  C
from snow import exc, model
from snow.ptscreen import pscr
from snow.request import parse_query, Query
from snow.tracking import tracking
from snow.util import make_zip_response, to_yaml, make_json_response

logger = logging.getLogger(__name__)


class ExportOptions(object):
    def __init__(self, query: Query, label=None, description=None, userid=None, data_version=None):
        self.query = query
        self.label = label
        self.description = description
        self.userid = userid
        self.data_version = data_version

    def create_metadata(self):
        metadata = dict()

        if self.query is not None:
            if self.query.filters is not None:
                metadata[C.FILTERS] = self.query.filters.filters

            if self.query.sites is not None:
                metadata.update(self._create_site_metadata(self.query.sites))

            if self.query.limits is not None:
                metadata.update(self._create_limit_metadata(self.query.limits))

        if self.label is not None:
            metadata[C.EXPORT_LABEL] = self.label

        if self.description is not None:
            metadata[C.EXPORT_DESCRIPTION] = self.description

        if self.userid is not None:
            metadata[C.EXPORT_USER] = self.userid

        if self.data_version is not None:
            metadata[C.DATA_VERSION] = self.data_version

        return metadata

    def _create_site_metadata(self, sites):
        metadata = dict()

        if sites.sites is not None and sites.cutoffs is not None:
            metadata[C.YMCA_SITES] = {
                site: cutoff
                for site, cutoff in zip(sites.sites, sites.cutoffs)
            }
        elif sites.sites != sites.cutoffs:
            raise exc.RSError('sites and cutoffs must both be present or both be None')

        return metadata

    def _create_limit_metadata(self, limits):
        metadata = dict()

        if limits.limit is not None:
            metadata[C.PATIENT_SUBSET] = {
                C.QK_EXPORT_LIMIT: limits.limit,
                C.QK_EXPORT_ORDER_BY: limits.order_by,
                C.QK_EXPORT_ORDER_ASC: limits.order_asc
            }

        return metadata


class ExportData(object):
    def __init__(self, options, patients, identifier=None, timestamp=None):
        self.options = options
        self.patients = patients
        self.identifier = identifier or str(uuid.uuid4())
        self.timestamp = timestamp or str(time.time())
        self.flags = C.EP_FLAG_VALUES

    def create_export_payload(self):
        return {
            C.EP_ID: self.identifier,
            C.EP_TS: self.timestamp,
            C.EP_SUBJECTS: self.patients[C.COL_PTNUM].tolist(),
            C.EP_METADATA: self.options.create_metadata(),
            C.EP_FLAGS: self.flags
        }

    def create_download_payload(self):
        patient_ids = self.patients[C.COL_PTNUM]

        files = {
            C.EXPORT_FILE_PATIENTS: patient_ids.to_csv(index=False),
            C.EXPORT_FILE_METADATA: to_yaml(self.options.create_metadata())
        }

        return make_zip_response(C.EXPORT_FILENAME, files)


def parse_export_identifiers(args: dict):
    label = None
    description = None
    userid = None

    if C.EXPORT_LABEL in args:
        label = args.pop(C.EXPORT_LABEL)
    if C.EXPORT_DESCRIPTION in args:
        description = args.pop(C.EXPORT_DESCRIPTION)
    if C.EXPORT_USER in args:
        userid = args.pop(C.EXPORT_USER)

    return label, description, userid


def parse_export_options(args: dict) -> ExportOptions:
    query = parse_query(args, site_required=False)
    label, description, userid = parse_export_identifiers(query.unused)
    data_version = model.cdm.data_version

    return ExportOptions(query, label=label, description=description, userid=userid, data_version=data_version)


def prepare_export_data():
    opts = parse_export_options(request.args)

    patients = pscr.filter_patients(opts.query)

    return ExportData(opts, patients)


def download_patients():
    export_data = prepare_export_data()

    return export_data.create_download_payload()


def export_patients():
    export_data = prepare_export_data()
    payload = export_data.create_export_payload()

    try:
        return make_json_response(tracking.export_data(payload))
    except exc.RSExportError as e:
        logger.error('export failed: %s', e)
        return make_json_response(str(e), status=500)
    except Exception as e:
        logger.error('export failed: %s', e)
        return make_json_response('export failed for unrecognized reason', status=500)
