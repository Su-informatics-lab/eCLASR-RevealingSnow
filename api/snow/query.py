import itertools
import logging

import yaml
from flask import request

from snow import constants as  C
from snow import model
from snow import stats, ymca
from snow.exc import RSError
from snow.filters import validate_filters
from snow.ptscreen import pscr
from snow.util import make_json_response, make_zip_response
from snow.ymca import SiteMode

logger = logging.getLogger(__name__)


def _validate_nested_keys(keys):
    invalid_keys = list(filter(lambda x: x.count('.') > 1, keys))
    if len(invalid_keys) > 0:
        raise RSError('multi-level query args are not supported: [{}]'.format(
            ', '.join(invalid_keys)
        ))


def _get_nested_key_groups(nested_keys):
    keyfunc = lambda x: x.split('.')[0]
    keys = sorted(nested_keys, key=keyfunc)

    return itertools.groupby(keys, keyfunc)


def _build_nested_args(args, nested_keys):
    _validate_nested_keys(nested_keys)
    grouped_keys = _get_nested_key_groups(nested_keys)
    nested_args = {
        prefix: {
            key.split('.')[1]: args[key]
            for key in group
        }
        for prefix, group in grouped_keys
    }

    return nested_args


def _split_sites_and_cutoffs(site, cutoff):
    if ',' in site:
        site = site.split(',')
    else:
        site = [site]

    if cutoff is not None:
        if ',' in cutoff:
            cutoff = [int(value) for value in cutoff.split(',')]
        else:
            cutoff = [int(cutoff)]

    return site, cutoff


def _validate_ymca_sites_and_cutoffs(sites, cutoffs):
    if len(sites) != len(cutoffs):
        raise RSError(
            "number of YMCA sites ({}) must match number of cutoffs ({})".format(
                len(sites), len(cutoffs)
            )
        )

    for site in sites:
        if site not in model.cdm.ymca_site_keys:
            raise RSError("invalid YMCA site: '{}'".format(site))


def parse_query_args(args: dict) -> dict:
    if not args:
        return args

    keys = set(args.keys())
    nested_keys = set(filter(lambda x: '.' in x, keys))
    simple_keys = keys.difference(nested_keys)

    nested_args = _build_nested_args(args, nested_keys)

    invalid_keys = simple_keys.intersection(nested_args.keys())
    if len(invalid_keys) > 0:
        raise RSError(
            'field(s) cannot have both simple value and nested value: [{}]'.format(
                ', '.join(invalid_keys)
            )
        )

    args = {key: args[key] for key in simple_keys}
    args.update(nested_args)

    return args


def parse_ymca_args(args: dict):
    # Validate that the required 'site' argument is present
    if C.QK_SITE in args:
        site = args.pop(C.QK_SITE)
    else:
        raise RSError("missing required argument: '{}'".format(C.QK_SITE))

    # Pull out the 'cutoff' argument if present
    if C.QK_CUTOFF in args:
        cutoff = args.pop(C.QK_CUTOFF)
    else:
        raise RSError("missing required argument: '{}'".format(C.QK_CUTOFF))

    site, cutoff = _split_sites_and_cutoffs(site, cutoff)
    _validate_ymca_sites_and_cutoffs(site, cutoff)

    return site, cutoff


def parse_ymca_query_args(args: dict, site_required=True):
    args = parse_query_args(args)
    if site_required or C.QK_SITE in args:
        site, cutoff = parse_ymca_args(args)
    else:
        site, cutoff = None, None

    # Return a tuple of the site(s), the cutoff(s) (optionally None), and the remaining filters
    return site, cutoff, args


def patient_stats():
    sites, cutoffs, filters = parse_ymca_query_args(request.args, site_required=False)
    validate_filters(filters)

    patients = pscr.filter_patients(filters)
    if sites is not None:
        patients = ymca.filter_by_distance(patients, sites, cutoffs, mode=SiteMode.ANY)

    ptstats = stats.patient_counts_by_category(patients)

    return make_json_response(ptstats)


def ymca_stats():
    site, cutoff, filters = parse_ymca_query_args(request.args)
    validate_filters(filters)

    patients = pscr.filter_patients(filters)
    dist_stats = ymca.get_ymca_distance_stats(patients, site, cutoff, ymca.YMCA_DEMOGRAPHIC_CATEGORIES)

    return make_json_response(dist_stats)


def export_patients():
    sites, cutoffs, filters = parse_ymca_query_args(request.args, site_required=False)
    validate_filters(filters)

    patients = pscr.filter_patients(filters)

    if sites is not None:
        patients = ymca.filter_by_distance(patients, sites, cutoffs, mode=SiteMode.ANY)

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
        _validate_ymca_sites_and_cutoffs(sites, cutoffs)
        metadata[C.YMCA_SITES] = {
            site: cutoff
            for site, cutoff in zip(sites, cutoffs)
        }
    elif sites != cutoffs:
        raise RSError('sites and cutoffs must both be present or both be None')

    return yaml.safe_dump(metadata, default_flow_style=False, explicit_start=True)
