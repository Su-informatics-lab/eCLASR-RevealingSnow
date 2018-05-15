import pandas as pd

_IDENTITY = lambda x: x
_ROUND = lambda x: x.round()

CATEGORIES = {
    'sex': _IDENTITY,
    'race': _IDENTITY,
    'ethnicity': _IDENTITY,
    'age': _ROUND,
}


def _get_available_categories(pscr: pd.DataFrame) -> set:
    available_columns = set(pscr.columns.values)
    return available_columns.intersection(set(CATEGORIES))


def _get_category_counts(pscr: pd.DataFrame, column: str) -> dict:
    values = pscr[column]
    values = CATEGORIES[column](values)

    return values.value_counts().to_dict()


def patient_counts_by_category(pscr: pd.DataFrame) -> dict:
    categories = _get_available_categories(pscr)

    # pscr.groupby(category).size().to_dict()
    return {
        category: _get_category_counts(pscr, category)
        for category in categories
    }
