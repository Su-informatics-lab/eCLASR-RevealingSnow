import logging
from os import path
from typing import List

import numpy as np
import pandas as pd

from snow import constants as C
from snow.filters import filter_patients
from snow.request import Query

logger = logging.getLogger(__name__)


def _round_ymca_columns(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    return np.ceil(data[columns])


def _pre_process(data: pd.DataFrame) -> pd.DataFrame:
    ymca_columns = [column for column in data.columns if column.startswith(C.COL_YMCA_PREFIX)]
    data.update(_round_ymca_columns(data, ymca_columns))

    return data


class PatientScreeningData(object):
    def __init__(self):
        self.pscr = None

    def init_app(self, app):
        if C.SCREENING_DATA_FILE not in app.config:
            logger.warning('{} is not set; no data will be loaded'.format(C.SCREENING_DATA_FILE))

        self._load_screening_table(app.config[C.SCREENING_DATA_FILE])

    def _load_screening_table(self, filename: str):
        logger.debug("Loading patient screening data from %s", filename)

        if not path.exists(filename):
            logger.warning('Screening file %s does not exist; no data will be loaded', filename)
        else:
            self.pscr = _pre_process(pd.read_csv(filename, low_memory=False))
            logger.debug('Loaded %d records', self.pscr.shape[0])

    def filter_patients(self, query: Query) -> pd.DataFrame:
        return filter_patients(self.pscr, query)


pscr = PatientScreeningData()
