import logging
import time
import uuid

import pandas as pd
from flask import request

from snow import constants as  C
from snow import exc
from snow import ymca
from snow.filters import validate_filters
from snow.ptscreen import pscr
from snow.query import parse_ymca_query_args
from snow.tracking import tracking
from snow.util import make_zip_response, parse_boolean, to_yaml, make_json_response

logger = logging.getLogger(__name__)

class ExportOptions(object):
    def __init__(self,
                 sites, cutoffs, filters,
                 limit, order_by, order_asc):
        self.sites = sites
        self.cutoffs = cutoffs
        self.filters = filters

        self.limit = limit
        self.order_by = order_by
        self.order_asc = order_asc

    def create_metadata(self):
        metadata = {
            C.FILTERS: self.filters
        }

        if self.sites is not None and self.cutoffs is not None:
            ymca._validate_ymca_sites_and_cutoffs(self.sites, self.cutoffs)
            metadata[C.YMCA_SITES] = {
                site: cutoff
                for site, cutoff in zip(self.sites, self.cutoffs)
            }
        elif self.sites != self.cutoffs:
            raise exc.RSError('sites and cutoffs must both be present or both be None')

        if self.limit is not None:
            metadata[C.PATIENT_SUBSET] = {
                C.QK_EXPORT_LIMIT: self.limit,
                C.QK_EXPORT_ORDER_BY: self.order_by,
                C.QK_EXPORT_ORDER_ASC: self.order_asc
            }

        return metadata


class ExportData(object):
    def __init__(self, options, patients, identifier=None, timestamp=None):
        self.options = options
        self.patients = patients
        self.identifier = identifier or str(uuid.uuid4())
        self.timestamp = timestamp or str(time.time())

    def create_export_payload(self):
        return {
            C.EP_ID: self.identifier,
            C.EP_TS: self.timestamp,
            C.EP_SUBJECTS: self.patients[C.COL_PTNUM].tolist(),
            C.EP_METADATA: self.options.create_metadata()
        }

    def create_download_payload(self):
        files = {
            C.EXPORT_FILE_PATIENTS: self.patients.to_csv(index=False),
            C.EXPORT_FILE_METADATA: to_yaml(self.options.create_metadata())
        }

        return make_zip_response(C.EXPORT_FILENAME, files)


def parse_export_limits(args: dict):
    limit = None
    order_by = None
    order_asc = False

    if C.QK_EXPORT_LIMIT in args:
        if C.QK_EXPORT_ORDER_BY not in args:
            raise exc.RSError('export limit requires {} argument'.format(C.QK_EXPORT_ORDER_BY))

        limit = args.pop(C.QK_EXPORT_LIMIT)
        order_by = args.pop(C.QK_EXPORT_ORDER_BY)
        order_asc = parse_boolean(args.pop(C.QK_EXPORT_ORDER_ASC, False))

        try:
            limit = int(limit)
        except ValueError:
            raise exc.RSError("invalid export limit '{}'".format(limit))

        if order_by not in C.QK_EXPORT_ORDER_VALUES:
            raise exc.RSError("invalid order field '{}'".format(order_by))

    return limit, order_by, order_asc


def parse_export_options(args: dict) -> ExportOptions:
    sites, cutoffs, filters = parse_ymca_query_args(args, site_required=False)
    limit, order_by, order_asc = parse_export_limits(filters)

    return ExportOptions(sites, cutoffs, filters, limit, order_by, order_asc)


def limit_patient_set(patients: pd.DataFrame, limit, order_by, order_asc):
    if limit is None:
        return patients

    if not order_by:
        raise exc.RSError('order required when limit is specified')

    if order_by not in patients.columns:
        raise exc.RSError("missing order column: '{}'".format(order_by))

    patients = patients.sort_values(by=[order_by], ascending=order_asc)
    return patients.head(limit)


def prepare_export_data():
    opts = parse_export_options(request.args)

    validate_filters(opts.filters)

    patients = pscr.filter_patients(opts.filters)

    if opts.sites is not None:
        patients = ymca.filter_by_distance(patients, opts.sites, opts.cutoffs, mode=ymca.SiteMode.ANY)

    if opts.limit is not None:
        patients = limit_patient_set(patients, opts.limit, opts.order_by, opts.order_asc)

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
