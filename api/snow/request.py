import itertools
import logging
from typing import Optional

from snow import constants as  C, model
from snow import exc
from snow.exc import RSError
from snow.util import parse_boolean

logger = logging.getLogger(__name__)



class SiteArguments(object):
    def __init__(self, sites, cutoffs):
        self.sites = sites
        self.cutoffs = cutoffs


class LimitArguments(object):
    def __init__(self, limit, order_by, order_asc):
        self.limit = limit
        self.order_by = order_by
        self.order_asc = order_asc


class FilterArguments(object):
    def __init__(self, filters):
        self.filters = filters


class Query(object):
    def __init__(self, filters: FilterArguments, sites: SiteArguments, limits: LimitArguments,
                 unused: Optional[dict] = None):
        self.filters = filters
        self.sites = sites
        self.limits = limits
        self.unused = unused


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


def validate_filters(filters: dict):
    valid_filter_keys = model.cdm.filter_keys

    for key, value in filters.items():
        if key not in valid_filter_keys:
            raise RSError("invalid filter key '{}'".format(key))

        filter = model.cdm.get_filter(key)
        filter.validate_filter_value(value)


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


def simplify_query_args(args: dict) -> dict:
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


def parse_site_arguments(args, site_required=False) -> Optional[SiteArguments]:
    if site_required or C.QK_SITE in args:
        site, cutoff = parse_ymca_args(args)
    else:
        site = None
        cutoff = None

    return SiteArguments(site, cutoff)


def parse_limit_arguments(args: dict) -> LimitArguments:
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

    return LimitArguments(limit, order_by, order_asc)


def parse_filter_arguments(args: dict) -> FilterArguments:
    filters = dict()
    valid_filter_keys = model.cdm.filter_keys

    for key in valid_filter_keys:
        if key in args:
            filters[key] = args.pop(key)

    validate_filters(filters)

    return FilterArguments(filters)


def parse_query(args: dict, site_required=False) -> Query:
    args = simplify_query_args(args)

    site_arguments = parse_site_arguments(args, site_required)
    limit_arguments = parse_limit_arguments(args)
    filter_arguments = parse_filter_arguments(args)

    return Query(filter_arguments, site_arguments, limit_arguments, args)
