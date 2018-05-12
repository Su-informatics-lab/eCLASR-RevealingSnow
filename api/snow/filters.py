import pandas as pd

from snow import model
from snow.exc import RSError

_CRITERION_DATE_CONJUNCTION = {
    '0': 'or',
    '1': 'and'
}

_CRITERION_DATE_COMPARISON = {
    '0': '<',
    '1': '>='
}

_VALID_FILTER_VALUES = {'0', '1'}


def _date_field(key):
    return "{}_date".format(key)


def _expand_filter(key, value):
    # TODO: Remove this and replace with a more robust distance filtering solution
    if key == 'ymca_fulton':
        return 'ymca_fulton < {value}'.format(value=value)

    if not isinstance(value, dict):
        return '{} == {}'.format(key, value)

    date_field = _date_field(key)
    field_value = value['value']
    date_value = value['date']
    date_comp = _CRITERION_DATE_COMPARISON[field_value]
    conjunction = _CRITERION_DATE_CONJUNCTION[field_value]

    return '({field} == {value} {conj} {date_field} {date_comp} "{date_value}")'.format(
        field=key,
        value=field_value,
        conj=conjunction,
        date_field=date_field,
        date_comp=date_comp,
        date_value=date_value
    )


def filter_patients(data: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if filters:
        condition = [
            _expand_filter(key, value)
            for key, value in filters.items()
        ]
        data = data.query(' and '.join(condition))

    return data


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
        # TODO: Repalce with more robust distance validation
        if key == 'ymca_fulton':
            continue
        if key not in valid_filter_keys:
            raise RSError("invalid filter key '{}'".format(key))

        _validate_filter(value)
