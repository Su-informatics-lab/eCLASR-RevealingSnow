from unittest import TestCase

import pandas as pd
from parameterized import parameterized

from snow import filters


class FilterTests(TestCase):
    def setUp(self):
        super(FilterTests, self).setUp()

        data = {
            'patient_num': [1, 2, 3],
            'cardiac': [0, 0, 1],
            'cardiac_date': [None, None, '2018-05-01'],
            'neuro': [0, 1, 1],
            'neuro_date': [None, '2018-04-01', '2018-06-01']
        }
        self.data = pd.DataFrame(data=data)

    def test_empty_filter_returns_full_dataset(self):
        result = filters.filter_patients(self.data, dict())
        self.assertTrue(self.data.equals(result))

    @parameterized.expand([
        (0, {1, 2}),
        (1, {3}),
    ])
    def test_filter_value_subsets_dataset(self, cardiac_value, expected_patient_nums):
        result = filters.filter_patients(self.data, {'cardiac': cardiac_value})
        actual_patient_nums = result['patient_num']
        self.assertEqual(set(actual_patient_nums.values), expected_patient_nums)

    def test_multiple_filters_treated_as_and(self):
        result = filters.filter_patients(self.data, {'cardiac': 1, 'neuro': 1})
        self.assertEqual(result['patient_num'].values, [3])
