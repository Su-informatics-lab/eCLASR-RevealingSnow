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


def parse_export_limits(args: dict):
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


def parse_export_options(args: dict) -> ExportOptions:
    sites, cutoffs, filters = parse_ymca_query_args(args, site_required=False)
    limit, order_by, order_asc = parse_export_limits(filters)

    return ExportOptions(sites, cutoffs, filters, limit, order_by, order_asc)


def limit_patient_set(patients: pd.DataFrame, limit, order_by, order_asc):
    if limit is None:
        return patients

    if not order_by:
        raise RSError('order required when limit is specified')

    if order_by not in patients.columns:
        raise RSError("missing order column: '{}'".format(order_by))

    patients = patients.sort_values(by=[order_by], ascending=order_asc)
    return patients.head(limit)


def download_patients():
    opts = parse_export_options(request.args)

    validate_filters(opts.filters)

    patients = pscr.filter_patients(opts.filters)

    if opts.sites is not None:
        patients = ymca.filter_by_distance(patients, opts.sites, opts.cutoffs, mode=SiteMode.ANY)

    if opts.limit is not None:
        patients = limit_patient_set(patients, opts.limit, opts.order_by, opts.order_asc)

    files = {
        C.EXPORT_FILE_PATIENTS: patients.to_csv(index=False),
        C.EXPORT_FILE_METADATA: create_metadata_from_export_options(opts)
    }

    return make_zip_response(C.EXPORT_FILENAME, files)


def create_metadata_from_export_options(options: ExportOptions):
    metadata = {
        C.FILTERS: options.filters
    }

    if options.sites is not None and options.cutoffs is not None:
        ymca._validate_ymca_sites_and_cutoffs(options.sites, options.cutoffs)
        metadata[C.YMCA_SITES] = {
            site: cutoff
            for site, cutoff in zip(options.sites, options.cutoffs)
        }
    elif options.sites != options.cutoffs:
        raise RSError('sites and cutoffs must both be present or both be None')

    if options.limit is not None:
        metadata[C.PATIENT_SUBSET] = {
            C.QK_EXPORT_LIMIT: options.limit,
            C.QK_EXPORT_ORDER_BY: options.order_by,
            C.QK_EXPORT_ORDER_ASC: options.order_asc
        }

    return yaml.safe_dump(metadata, default_flow_style=False, explicit_start=True)
