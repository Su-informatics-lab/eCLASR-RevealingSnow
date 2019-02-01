from typing import List

import pandas as pd

import snow.constants as C
from snow.exc import RSError

YMCA_DEMOGRAPHIC_CATEGORIES = {C.COL_SEX, C.COL_RACE, C.COL_ETHNICITY}


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


def get_ymca_distance_stats(pscr: pd.DataFrame, sites: List[str], maxdists: List[int],
                            categories: List[str] = None) -> dict:
    """
    :param categories: A list of demographic categories to summarize in addition to overall distances.
    """
    if len(sites) > 1:
        raise RSError('get_ymca_distance_stats does not support multiple sites')

    return _get_distance_counts(pscr, sites[0], categories)
