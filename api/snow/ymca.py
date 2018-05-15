from typing import Optional

import pandas as pd


def _filter_by_distance(data: pd.DataFrame, site: str, cutoff: Optional[int]) -> pd.DataFrame:
    if cutoff:
        data = data.query('{site} < {cutoff}'.format(site=site, cutoff=cutoff))

    return data


def _get_distance_counts(data: pd.DataFrame, site: str) -> dict:
    values = data[site]
    values = values.round()
    value_counts = values.value_counts().to_dict()

    return {
        site: value_counts
    }


def get_ymca_distance_stats(pscr: pd.DataFrame, site: str, cutoff: Optional[int] = None) -> dict:
    pscr = _filter_by_distance(pscr, site, cutoff)

    return _get_distance_counts(pscr, site)
