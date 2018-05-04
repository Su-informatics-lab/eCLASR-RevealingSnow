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

    def _get_filtered_patient_nums(self, f):
        result = filters.filter_patients(self.data, f)
        return set(result['patient_num'].values)

    def test_empty_filter_returns_full_dataset(self):
        result = filters.filter_patients(self.data, dict())
        self.assertTrue(self.data.equals(result))

    @parameterized.expand([
        ('0', {1, 2}),
        ('1', {3}),
    ])
    def test_filter_value_subsets_dataset(self, cardiac_value, expected_patient_nums):
        actual_patient_nums = self._get_filtered_patient_nums({'cardiac': cardiac_value})
        self.assertEqual(actual_patient_nums, expected_patient_nums)

    def test_multiple_filters_treated_as_and(self):
        patient_nums = self._get_filtered_patient_nums({'cardiac': '1', 'neuro': '1'})
        self.assertEqual(patient_nums, {3})

    def test_exclusion_with_date_excludes_patients_with_condition_after_cutoff(self):
        patient_nums = self._get_filtered_patient_nums({'neuro': {'value': '0', 'date': '2018-05-01'}})
        self.assertEqual(patient_nums, {1, 2})

    def test_inclusion_with_date_includes_patients_with_condition_after_cutoff(self):
        patient_nums = self._get_filtered_patient_nums({'neuro': {'value': '1', 'date': '2018-05-01'}})
        self.assertEqual(patient_nums, {3})
