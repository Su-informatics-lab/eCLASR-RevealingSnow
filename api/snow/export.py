import pandas as pd
import yaml
from flask import request

from snow import constants as  C
from snow import ymca
from snow.exc import RSError
from snow.filters import validate_filters
from snow.ptscreen import pscr
from snow.query import parse_ymca_query_args
from snow.util import make_zip_response, parse_boolean
from snow.ymca import SiteMode


def parse_export_options(args: dict):
    limit = None
    order_by = None
    order_asc = False

    if C.QK_EXPORT_LIMIT in args:
        if C.QK_EXPORT_ORDER_BY not in args:
            raise RSError('export limit requires {} argument'.format(C.QK_EXPORT_ORDER_BY))

        limit = args.pop(C.QK_EXPORT_LIMIT)
        order_by = args.pop(C.QK_EXPORT_ORDER_BY)
        order_asc = parse_boolean(args.pop(C.QK_EXPORT_ORDER_ASC, False))

        try:
            limit = int(limit)
        except ValueError:
            raise RSError("invalid export limit '{}'".format(limit))

        if order_by not in C.QK_EXPORT_ORDER_VALUES:
            raise RSError("invalid order field '{}'".format(order_by))

    return limit, order_by, order_asc


def limit_patient_set(patients: pd.DataFrame, limit, order_by):
    if limit is None:
        return patients

    if not order_by:
        raise RSError('order required when limit is specified')

    if order_by not in patients.columns:
        raise RSError("missing order column: '{}'".format(order_by))

    patients = patients.sort_values(by=[order_by], ascending=False)
    return patients.head(limit)


def export_patients():
    sites, cutoffs, filters = parse_ymca_query_args(request.args, site_required=False)
    limit, order, _ = parse_export_options(filters)

    validate_filters(filters)

    patients = pscr.filter_patients(filters)

    if sites is not None:
        patients = ymca.filter_by_distance(patients, sites, cutoffs, mode=SiteMode.ANY)

    if limit is not None:
        patients = limit_patient_set(patients, limit, order)

    files = {
        C.EXPORT_FILE_PATIENTS: patients.to_csv(index=False),
        C.EXPORT_FILE_METADATA: create_metadata_from_parameters(sites, cutoffs, filters)
    }

    return make_zip_response(C.EXPORT_FILENAME, files)


def create_metadata_from_parameters(sites, cutoffs, filters):
    metadata = {
        C.FILTERS: filters
    }

    if sites is not None and cutoffs is not None:
        ymca._validate_ymca_sites_and_cutoffs(sites, cutoffs)
        metadata[C.YMCA_SITES] = {
            site: cutoff
            for site, cutoff in zip(sites, cutoffs)
        }
    elif sites != cutoffs:
        raise RSError('sites and cutoffs must both be present or both be None')

    return yaml.safe_dump(metadata, default_flow_style=False, explicit_start=True)
