import pandas as pd

CATEGORIES = [
    'sex', 'race', 'ethnicity'
]


def patient_counts_by_category(pscr: pd.DataFrame) -> dict:
    return {
        category: pscr.groupby(category).size().to_dict()
        for category in CATEGORIES
    }
