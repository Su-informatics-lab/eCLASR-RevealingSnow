import logging
from os import path

import pandas as pd

logger = logging.getLogger(__name__)


class PatientScreeningData(object):
    def __init__(self):
        self.pscr = None

    def init_app(self, app):
        if 'SCREENING_DATA_FILE' not in app.config:
            logger.warning('SCREENING_DATA_FILE is not set; no data will be loaded')

        self.load_screening_table(app.config['SCREENING_DATA_FILE'])

    def load_screening_table(self, filename: str):
        logger.debug("Loading patient screening data from %s", filename)

        if not path.exists(filename):
            logger.warning('Screening file %s does not exist; no data will be loaded', filename)
        else:
            self.pscr = pd.read_csv(filename, low_memory=False)
            logger.debug('Loaded %d records', self.pscr.shape[0])


pscr = PatientScreeningData()
