import pandas as pd

_CRITERION_DATE_CONJUNCTION = {
    '0': 'or',
    '1': 'and'
}

_CRITERION_DATE_COMPARISON = {
    '0': '<',
    '1': '>='
}


def _date_field(key):
    return "{}_date".format(key)


def _expand_filter(key, value):
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
