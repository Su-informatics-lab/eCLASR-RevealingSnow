import itertools
import logging
from typing import Optional

from snow import constants as  C, model
from snow import ymca, exc
from snow.exc import RSError
from snow.util import parse_boolean

logger = logging.getLogger(__name__)

_VALID_FILTER_VALUES = {'0', '1'}


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


def _validate_filter_value(value):
    if value not in _VALID_FILTER_VALUES:
        raise RSError("invalid filter value '{}'; must be one of [{}]".format(
            value, ', '.join(_VALID_FILTER_VALUES)
        ))


def _validate_filter(value):
    if not isinstance(value, dict):
        _validate_filter_value(value)
    else:
        if 'value' not in value:
            raise RSError("filter value structure must contain 'value' element")

        _validate_filter_value(value['value'])


def validate_filters(filters: dict):
    valid_filter_keys = model.cdm.filter_keys

    for key, value in filters.items():
        if key not in valid_filter_keys:
            raise RSError("invalid filter key '{}'".format(key))

        _validate_filter(value)


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


def parse_ymca_query_args(args: dict, site_required=True):
    args = simplify_query_args(args)
    if site_required or C.QK_SITE in args:
        site, cutoff = ymca.parse_ymca_args(args)
    else:
        site, cutoff = None, None

    # Return a tuple of the site(s), the cutoff(s) (optionally None), and the remaining filters
    return site, cutoff, args


def parse_site_arguments(args, site_required=False) -> Optional[SiteArguments]:
    if site_required or C.QK_SITE in args:
        site, cutoff = ymca.parse_ymca_args(args)
        return SiteArguments(site, cutoff)

    return None


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
