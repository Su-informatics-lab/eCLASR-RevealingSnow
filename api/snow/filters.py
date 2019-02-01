from enum import Enum

import pandas as pd

import snow.constants as C
from snow import exc, model
from snow.request import Query, FilterArguments, SiteArguments, LimitArguments


class SiteMode(Enum):
    ALL = ' and '
    ANY = ' or '


def filter_patients_by_distance(data: pd.DataFrame, site_args: SiteArguments,
                                mode: SiteMode = SiteMode.ALL) -> pd.DataFrame:
    if site_args is None or site_args.sites is None:
        return data

    criteria = mode.value.join([
        '{site} <= {maxdist}'.format(site=site, maxdist=maxdist)
        for site, maxdist in zip(site_args.sites, site_args.maxdists)
    ])

    data = data.query(criteria)

    return data


def filter_patients_by_emr_criteria(data: pd.DataFrame, filter_args: FilterArguments) -> pd.DataFrame:
    if filter_args and filter_args.filters:
        condition = [
            model.cdm.get_filter(key).expand_filter_expression(key, value)
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
            sites = list(model.cdm.ymca_site_keys)
        else:
            sites = sites.sites

        closest_site = patients[sites].min(axis=1)
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
