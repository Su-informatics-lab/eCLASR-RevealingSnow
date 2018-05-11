from unittest import TestCase

import pandas as pd

from snow import stats


class StatsTests(TestCase):
    def setUp(self):
        super(StatsTests, self).setUp()

        pscr = {
            'patient_num': [1, 2, 3],
            'sex': ['M', 'F', 'F'],
            'age': [73.35, 72.75, 65.05]
        }
        self.pscr = pd.DataFrame(data=pscr)

    def test_categorical_stats(self):
        expected = {'M': 1, 'F': 2}
        actual = stats.patient_counts_by_category(self.pscr)

        self.assertEqual(actual['sex'], expected)

    def test_numeric_binning(self):
        expected = {73.0: 2, 65.0: 1}
        actual = stats.patient_counts_by_category(self.pscr)

        self.assertEqual(actual['age'], expected)
