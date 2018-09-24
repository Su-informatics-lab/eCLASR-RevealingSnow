from unittest import TestCase

import pandas as pd
import yaml
from parameterized import parameterized

from snow import constants as C
from snow import export
from snow.exc import RSError


class ExportOptionParserTests(TestCase):
    def _parse_opts(self, limit, order, **kwargs):
        args = {
            C.QK_EXPORT_LIMIT: limit,
            C.QK_EXPORT_ORDER_BY: order,
        }
        args.update(kwargs)

        return export.parse_export_options(args)

    def test_args_without_export_options_returns_none(self):
        limit, order_by, _ = export.parse_export_options({'foo': 'bar'})

        self.assertIsNone(limit)
        self.assertIsNone(order_by)

    def test_export_limit_without_order_by_raises_exception(self):
        with self.assertRaises(RSError) as e:
            export.parse_export_options({C.QK_EXPORT_LIMIT: '500'})

        self.assertIn(
            'export limit requires {} argument'.format(C.QK_EXPORT_ORDER_BY),
            str(e.exception)
        )

    def test_invalid_order_field_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._parse_opts(50, 'foobar')

        self.assertIn('invalid order field', str(e.exception))

    def test_invalid_limit_field_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._parse_opts('foobar', 'last_visit_date')

        self.assertIn('invalid export limit', str(e.exception))

    def test_export_limit_and_order_returned(self):
        limit, order_by, _ = export.parse_export_options({
            C.QK_EXPORT_LIMIT: 50,
            C.QK_EXPORT_ORDER_BY: 'last_visit_date',
            'foo': 'bar'
        })

        self.assertEqual(limit, 50)
        self.assertEqual(order_by, 'last_visit_date')

    def test_export_limit_and_order_removed_from_args(self):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: 'last_visit_date', 'foo': 'bar'}
        export.parse_export_options(args)

        self.assertEqual(args, {'foo': 'bar'})

    def test_order_asc_defaults_to_false(self):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: 'last_visit_date'}
        _, _, order_dir = export.parse_export_options(args)

        self.assertFalse(order_dir)

    @parameterized.expand([
        (None, False),
        (False, False),
        ('0', False),
        ('false', False),
        ('1', True),
        ('true', True),
        ('True', True),
        ('t', True),
        ('T', True)
    ])
    def test_order_asc_parsed_as_boolean(self, order_asc, expected):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: 'last_visit_date', C.QK_EXPORT_ORDER_ASC: order_asc}
        _, _, order_dir = export.parse_export_options(args)

        self.assertEqual(order_dir, expected)


class LimitPatientsTests(TestCase):
    def setUp(self):
        super(LimitPatientsTests, self).setUp()

        data = {
            'patient_num': [1, 2, 3],
            'last_visit_date': ['2017-01-01', '2016-06-01', '2018-08-08'],
        }

        self.data = pd.DataFrame(data=data)

    def _get_subset_patient_nums(self, limit, order_by, order_asc=False):
        result = export.limit_patient_set(self.data, limit, order_by, order_asc)
        return set(result['patient_num'].values)

    def test_no_limit_returns_same_data(self):
        pt_nums = self._get_subset_patient_nums(None, None)
        self.assertEqual(pt_nums, {1, 2, 3})

    def test_no_order_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._get_subset_patient_nums(5, None)

        self.assertIn('order required when limit is specified', str(e.exception))

    def test_limit_greater_than_length_returns_same_data(self):
        pt_nums = self._get_subset_patient_nums(5, 'last_visit_date')
        self.assertEqual(pt_nums, {1, 2, 3})

    def test_limit_zero_returns_empty_data_frame(self):
        result = export.limit_patient_set(self.data, 0, 'last_visit_date', False)
        self.assertEqual(result.size, 0)

    def test_order_by_missing_column_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._get_subset_patient_nums(5, 'foobar')

        self.assertIn('missing order column', str(e.exception))

    @parameterized.expand([
        (1, {3}),
        (2, {1, 3}),
        (3, {1, 2, 3})
    ])
    def test_limit_returns_patients_with_highest_values(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, 'last_visit_date')
        self.assertEqual(actual, expected)

    @parameterized.expand([
        (1, {2}),
        (2, {1, 2}),
        (3, {1, 2, 3})
    ])
    def test_limit_with_asc_true_returns_patients_with_lowest_values(self, limit, expected):
        actual = self._get_subset_patient_nums(limit, 'last_visit_date', True)
        self.assertEqual(actual, expected)


class MetadataTests(TestCase):
    def _round_trip(self, site, cutoff, filters, limit=None, order_by=None, order_asc=None):
        metadata = export.create_metadata_from_parameters(site, cutoff, filters, limit, order_by, order_asc)
        return yaml.safe_load(metadata)

    def test_empty_metadata(self):
        actual = self._round_trip(None, None, None)
        self.assertEqual(actual, {C.FILTERS: None})

    def test_metadata_from_sites_only_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._round_trip(['ymca_hanes'], None, None)

        self.assertIn('sites and cutoffs must both be present or both be None', str(e.exception))

    def test_metadata_from_cutoffs_only_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._round_trip(None, [5], None)

        self.assertIn('sites and cutoffs must both be present or both be None', str(e.exception))

    def test_metadata_from_sites_and_cutoffs(self):
        expected = {
            C.YMCA_SITES: {
                'ymca_fulton': 5,
                'ymca_davie': 10
            },
            C.FILTERS: None
        }

        actual = self._round_trip(['ymca_fulton', 'ymca_davie'], [5, 10], None)

        self.assertEqual(actual, expected)

    def test_metadata_from_filters(self):
        filters = {'hospice': '0', 'bariatric': {
            'value': '1',
            'date': '2018-01-01'
        }}

        expected = {
            C.FILTERS: filters
        }

        actual = self._round_trip(None, None, filters)

        self.assertEqual(actual, expected)

    def test_metadata_from_sites_cutoffs_and_filters(self):
        filters = {'hospice': '0', 'bariatric': {
            'value': '1',
            'date': '2018-01-01'
        }}

        expected = {
            C.YMCA_SITES: {
                'ymca_fulton': 5,
                'ymca_davie': 10
            },
            C.FILTERS: filters
        }

        actual = self._round_trip(['ymca_fulton', 'ymca_davie'], [5, 10], filters)

        self.assertEqual(actual, expected)

    def test_metadata_with_limit(self):
        expected = {
            C.FILTERS: None,
            C.PATIENT_SUBSET: {
                C.QK_EXPORT_LIMIT: 50,
                C.QK_EXPORT_ORDER_BY: 'foo',
                C.QK_EXPORT_ORDER_ASC: True
            }
        }

        actual = self._round_trip(None, None, None, 50, 'foo', True)

        self.assertEqual(actual, expected)
