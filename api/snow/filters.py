import pandas as pd


def filter_patients(data: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if filters:
        condition = [
            "{} == {}".format(key, value)
            for key, value in filters.items()
        ]
        data = data.query(' and '.join(condition))

    return data
