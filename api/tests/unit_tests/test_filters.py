from unittest import TestCase

import pandas as pd
from mock import patch
from parameterized import parameterized

from snow import constants as C
from snow import filters
from snow.exc import RSError
from snow.request import FilterArguments, LimitArguments, SiteArguments


class FilterByEmrCriteriaTests(TestCase):
    def setUp(self):
        super(FilterByEmrCriteriaTests, self).setUp()

        data = {
            'patient_num': [1, 2, 3],
            'cardio2': [0, 0, 1],
            'cardio2_date': [None, None, '2018-05-01'],
            'neuro2': [0, 1, 1],
            'neuro2_date': [None, '2018-04-01', '2018-06-01']
        }
        self.data = pd.DataFrame(data=data)

    def _get_filtered_patient_nums(self, f):
        result = filters.filter_patients_by_emr_criteria(self.data, FilterArguments(f))
        return set(result['patient_num'].values)

    def test_empty_filter_returns_full_dataset(self):
        result = filters.filter_patients_by_emr_criteria(self.data, FilterArguments(None))
        self.assertTrue(self.data.equals(result))

    @parameterized.expand([
        ('0', {1, 2}),
        ('1', {3}),
    ])
    def test_filter_value_subsets_dataset(self, cardio_value, expected_patient_nums):
        actual_patient_nums = self._get_filtered_patient_nums({'cardio2': cardio_value})
        self.assertEqual(actual_patient_nums, expected_patient_nums)

    def test_multiple_filters_treated_as_and(self):
        patient_nums = self._get_filtered_patient_nums({'cardio2': '1', 'neuro2': '1'})
        self.assertEqual(patient_nums, {3})

    def test_exclusion_with_date_excludes_patients_with_condition_after_cutoff(self):
        patient_nums = self._get_filtered_patient_nums({'neuro2': {'value': '0', 'date': '2018-05-01'}})
        self.assertEqual(patient_nums, {1, 2})

    def test_inclusion_with_date_includes_patients_with_condition_after_cutoff(self):
        patient_nums = self._get_filtered_patient_nums({'neuro2': {'value': '1', 'date': '2018-05-01'}})
        self.assertEqual(patient_nums, {3})


class LimitPatientsTests(TestCase):
    def setUp(self):
        super(LimitPatientsTests, self).setUp()

        data = {
            'patient_num': [1, 2, 3],
            C.QK_LIMIT_LAST_VISIT_DATE: ['2017-01-01', '2016-06-01', '2018-08-08'],
            'ymca_foo': [2, 3, 6],
            'ymca_bar': [4, 1, 5]
        }

        self.data = pd.DataFrame(data=data)

    def _get_subset_patient_nums(self, limit, order_by, order_asc=False, sites=None):
        limit_args = LimitArguments(limit, order_by, order_asc)
        site_args = SiteArguments(sites, None, 0)

        result = filters.limit_patient_set(self.data, limit_args, site_args)
        return set(result['patient_num'].values)

    def test_no_limit_returns_same_data(self):
        pt_nums = self._get_subset_patient_nums(None, None)
        self.assertEqual(pt_nums, {1, 2, 3})

    def test_no_order_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._get_subset_patient_nums(5, None)

        self.assertIn('order required when limit is specified', str(e.exception))

    def test_limit_greater_than_length_returns_same_data(self):
        pt_nums = self._get_subset_patient_nums(5, C.QK_LIMIT_LAST_VISIT_DATE)
        self.assertEqual(pt_nums, {1, 2, 3})

    def test_limit_zero_returns_empty_data_frame(self):
        result = self._get_subset_patient_nums(0, C.QK_LIMIT_LAST_VISIT_DATE, False)
        self.assertEqual(len(result), 0)

    def test_order_by_missing_column_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._get_subset_patient_nums(5, 'foobar')

        self.assertIn('missing order column', str(e.exception))

    @parameterized.expand([
        (1, {3}),
        (2, {1, 3}),
        (3, {1, 2, 3})
    ])
    def test_visit_date_limit_returns_patients_with_highest_values(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, C.QK_LIMIT_LAST_VISIT_DATE)
        self.assertEqual(actual, expected)

    @parameterized.expand([
        (1, {2}),
        (2, {1, 2}),
        (3, {1, 2, 3})
    ])
    def test_visit_date_limit_with_asc_true_returns_patients_with_lowest_values(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, C.QK_LIMIT_LAST_VISIT_DATE, True)
        self.assertEqual(actual, expected)

    @patch('snow.filters.model.cdm')
    def test_closest_ymca_without_sites_uses_all_sites(self, mock):
        # Mock the full CDM site keys to be the list of sites in the data set
        mock.ymca_site_keys = {'ymca_foo', 'ymca_bar'}

        actual = self._get_subset_patient_nums(2, C.QK_LIMIT_CLOSEST_YMCA, order_asc=True)

        self.assertEqual(actual, {2, 1})

    def test_closest_ymca_limit_only_uses_requested_sites(self):
        actual = self._get_subset_patient_nums(1, C.QK_LIMIT_CLOSEST_YMCA, order_asc=True, sites=['ymca_bar'])
        self.assertEqual(actual, {2})

    @parameterized.expand([
        (1, {3}),
        (2, {1, 3}),
        (3, {1, 2, 3})
    ])
    def test_closest_ymca_limit_returns_patients_with_greatest_distance(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, C.QK_LIMIT_CLOSEST_YMCA, sites=['ymca_foo', 'ymca_bar'])
        self.assertEqual(actual, expected)

    @parameterized.expand([
        (1, {2}),
        (2, {1, 2}),
        (3, {1, 2, 3})
    ])
    def test_closest_ymca_limit_with_asc_returns_patients_with_lowest_distance(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, C.QK_LIMIT_CLOSEST_YMCA, True, sites=['ymca_foo', 'ymca_bar'])
        self.assertEqual(actual, expected)


class YmcaFilterTests(TestCase):
    def setUp(self):
        super(YmcaFilterTests, self).setUp()

        pscr = {
            'patient_num': [1, 2, 3, 4],
            C.COL_SEX: ['M', 'F', 'M', 'F'],
            C.COL_RACE: ['W', 'W', 'B', 'B'],
            C.COL_ETHNICITY: ['N', 'U', 'U', 'N'],
            'ymca_fulton': [2, 3, 4, 4],
            'ymca_hanes': [8, 3, 2, 5],
        }
        self.pscr = pd.DataFrame(data=pscr)

    def test_filter_single_site_with_distance_range(self):
        actual = filters.filter_patients_by_distance(
            self.pscr,
            SiteArguments(['ymca_hanes'], [6], [2.5])
        )

        self.assertEqual(set(actual.patient_num), {2, 4})

    def test_filter_multiple_sites_with_all_mode(self):
        actual = filters.filter_patients_by_distance(
            self.pscr,
            SiteArguments(['ymca_fulton', 'ymca_hanes'], [3, 3], [0, 0]),
            mode=filters.SiteMode.ALL
        )

        self.assertEqual(set(actual.patient_num), {2})

    def test_filter_multiple_sites_with_any_mode(self):
        actual = filters.filter_patients_by_distance(
            self.pscr,
            SiteArguments(['ymca_fulton', 'ymca_hanes'], [3, 3], [0, 0]),
            mode=filters.SiteMode.ANY
        )

        self.assertEqual(set(actual.patient_num), {1, 2, 3})
