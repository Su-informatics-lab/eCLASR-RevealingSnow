from enum import Enum
from typing import List

import numpy as np
import pandas as pd

from snow.exc import RSError


class SiteMode(Enum):
    ALL = ' and '
    ANY = ' or '


def filter_by_distance(data: pd.DataFrame, sites: List[str], cutoffs: List[int],
                       mode: SiteMode = SiteMode.ALL) -> pd.DataFrame:
    criteria = mode.value.join([
        '{site} < {cutoff}'.format(site=site, cutoff=cutoff)
        for site, cutoff in zip(sites, cutoffs)
    ])

    data = data.query(criteria)

    return data


def _get_distance_counts(data: pd.DataFrame, site: str) -> dict:
    values = data[site]
    values = np.ceil(values)
    value_counts = values.value_counts().to_dict()

    return {
        site: value_counts
    }


def get_ymca_distance_stats(pscr: pd.DataFrame, sites: List[str], cutoffs: List[int]) -> dict:
    if len(sites) > 1:
        raise RSError('get_ymca_distance_stats does not support multiple sites')

    pscr = filter_by_distance(pscr, sites, cutoffs)
    return _get_distance_counts(pscr, sites[0])
