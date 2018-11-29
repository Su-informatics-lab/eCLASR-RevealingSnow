from typing import List

import pandas as pd

import snow.constants as C
from snow import model
from snow.exc import RSError

YMCA_DEMOGRAPHIC_CATEGORIES = {C.COL_SEX, C.COL_RACE, C.COL_ETHNICITY}


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


def _get_distance_counts_by_category(values, site, category):
    values = values.groupby(category)

    return {
        dist: counts[site].value_counts().to_dict()
        for dist, counts in values
    }


def _get_distance_counts(data: pd.DataFrame, site: str, categories: List[str] = None) -> dict:
    # Use the ceiling of the distances for grouping
    values = data.groupby(data[site])

    # Get overall totals, even if we're also going to get categories
    total_counts = values.size().to_dict()

    if not categories:
        value_counts = total_counts
    else:
        value_counts = {C.RK_TOTAL: total_counts}
        for category in categories:
            value_counts[category] = _get_distance_counts_by_category(data, site, category)

    return {
        site: value_counts
    }


def get_ymca_distance_stats(pscr: pd.DataFrame, sites: List[str], cutoffs: List[int],
                            categories: List[str] = None) -> dict:
    """
    :param categories: A list of demographic categories to summarize in addition to overall distances.
    """
    if len(sites) > 1:
        raise RSError('get_ymca_distance_stats does not support multiple sites')

    return _get_distance_counts(pscr, sites[0], categories)
