import logging
import time
import uuid

import pandas as pd
from flask import request

from snow import constants as  C
from snow import exc
from snow import ymca
from snow.ptscreen import pscr
from snow.request import parse_query, Query
from snow.tracking import tracking
from snow.util import make_zip_response, parse_boolean, to_yaml, make_json_response

logger = logging.getLogger(__name__)


class ExportOptions(object):
    def __init__(self, query: Query, label=None, description=None, userid=None):
        self.query = query
        self.label = label
        self.description = description
        self.userid = userid

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

        return metadata

    def _create_site_metadata(self, sites):
        metadata = dict()

        if sites.sites is not None and sites.cutoffs is not None:
            ymca._validate_ymca_sites_and_cutoffs(sites.sites, sites.cutoffs)
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


def parse_export_identifiers(args: dict):
    label = None
    description = None

    # Just a placeholder for now
    userid = C.EXPORT_USER

    if C.EXPORT_LABEL in args:
        label = args.pop(C.EXPORT_LABEL)
    if C.EXPORT_DESCRIPTION in args:
        description = args.pop(C.EXPORT_DESCRIPTION)

    return label, description, userid


def parse_export_options(args: dict) -> ExportOptions:
    query = parse_query(args, site_required=False)
    label, description, userid = parse_export_identifiers(query.unused)

    return ExportOptions(query, label=label, description=description, userid=userid)


def limit_patient_set(patients: pd.DataFrame, limit, order_by, order_asc, sites=None):
    if limit is None:
        return patients

    if not order_by:
        raise exc.RSError('order required when limit is specified')

    # Closest YMCA is a synthetic column based on the YMCA sites included in the query
    if order_by == C.QK_LIMIT_CLOSEST_YMCA:
        if sites is None:
            raise exc.RSError('at least one YMCA site must be selected when limiting by closest YMCA site')

        closest_site = patients[sites].min(axis=1)
        patients[C.QK_LIMIT_CLOSEST_YMCA] = closest_site

    if order_by not in patients.columns:
        raise exc.RSError("missing order column: '{}'".format(order_by))

    patients = patients.sort_values(by=[order_by], ascending=order_asc)
    return patients.head(limit)


def prepare_export_data():
    opts = parse_export_options(request.args)

    patients = pscr.filter_patients(opts.query.filters.filters)

    if opts.query.sites is not None:
        patients = ymca.filter_by_distance(patients, opts.query.sites.sites, opts.query.sites.cutoffs,
                                           mode=ymca.SiteMode.ANY)

    if opts.query.limits is not None:
        patients = limit_patient_set(
            patients,
            opts.query.limits.limit, opts.query.limits.order_by, opts.query.limits.order_asc,
            opts.query.sites.sites
        )

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
