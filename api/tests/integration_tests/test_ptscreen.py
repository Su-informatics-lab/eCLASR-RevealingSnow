from mock import MagicMock

from snow import constants as C
from snow.ptscreen import PatientScreeningData
from tests.integration_tests import TestBase


class PatientScreeningDataTests(TestBase):
    def setUp(self):
        super(PatientScreeningDataTests, self).setUp()

        self.ptdata = PatientScreeningData()
        self.app = MagicMock(config={
            C.SCREENING_DATA_FILE: self.get_data_file('pscr.csv')
        })

    def test_patient_data_empty_before_app_initialized(self):
        self.assertIsNone(self.ptdata.pscr)

    def test_patient_data_loaded_when_app_initialized(self):
        self.ptdata.init_app(self.app)
        self.assertIsNotNone(self.ptdata.pscr)

    def test_ymca_columns_rounded_up(self):
        self.ptdata.init_app(self.app)

        ymca_data = self.ptdata.pscr.ymca_foobar
        self.assertSequenceEqual(ymca_data.tolist(), [3, 5])
