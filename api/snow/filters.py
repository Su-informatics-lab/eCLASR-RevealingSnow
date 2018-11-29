from enum import Enum

import pandas as pd

import snow.constants as C
from snow import exc
from snow.request import Query, FilterArguments, SiteArguments, LimitArguments


class SiteMode(Enum):
    ALL = ' and '
    ANY = ' or '


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


def filter_patients_by_distance(data: pd.DataFrame, site_args: SiteArguments,
                                mode: SiteMode = SiteMode.ALL) -> pd.DataFrame:
    criteria = mode.value.join([
        '{site} < {cutoff}'.format(site=site, cutoff=cutoff)
        for site, cutoff in zip(site_args.sites, site_args.cutoffs)
    ])

    data = data.query(criteria)

    return data


def filter_patients_by_emr_criteria(data: pd.DataFrame, filter_args: FilterArguments) -> pd.DataFrame:
    if filter_args and filter_args.filters:
        condition = [
            _expand_filter(key, value)
            for key, value in filter_args.filters.items()
        ]
        data = data.query(' and '.join(condition))

    return data


def limit_patient_set(patients: pd.DataFrame, limit_args: LimitArguments, sites: SiteArguments = None):
    if limit_args is None or limit_args.limit is None:
        return patients

    if not limit_args.order_by:
        raise exc.RSError('order required when limit is specified')

    # Closest YMCA is a synthetic column based on the YMCA sites included in the query
    if limit_args.order_by == C.QK_LIMIT_CLOSEST_YMCA:
        if sites is None or sites.sites is None:
            raise exc.RSError('at least one YMCA site must be selected when limiting by closest YMCA site')

        closest_site = patients[sites.sites].min(axis=1)
        patients[C.QK_LIMIT_CLOSEST_YMCA] = closest_site

    if limit_args.order_by not in patients.columns:
        raise exc.RSError("missing order column: '{}'".format(limit_args.order_by))

    patients = patients.sort_values(by=[limit_args.order_by], ascending=limit_args.order_asc)
    return patients.head(limit_args.limit)


def filter_patients(patients: pd.DataFrame, query: Query) -> pd.DataFrame:
    if query.filters is not None:
        patients = filter_patients_by_emr_criteria(patients, query.filters)

    if query.sites is not None:
        patients = filter_patients_by_distance(patients, query.sites, mode=SiteMode.ANY)

    if query.limits is not None:
        patients = limit_patient_set(patients, query.limits, query.sites)

    return patients
