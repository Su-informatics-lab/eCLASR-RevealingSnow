import itertools
import logging

from flask import request

from snow import stats
from snow.exc import RSError
from snow.filters import validate_filters
from snow.ptscreen import pscr
from snow.util import make_json_response

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


def parse_query_args(args: dict):
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


def patient_stats():
    filters = parse_query_args(request.args)
    validate_filters(filters)

    patients = pscr.filter_patients(filters)
    ptstats = stats.patient_counts_by_category(patients)

    return make_json_response(ptstats)
