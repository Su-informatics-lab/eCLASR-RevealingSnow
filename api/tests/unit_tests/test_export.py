from unittest import TestCase

import yaml

from snow import constants as C
from snow import export
from snow.exc import RSError


class ExportOptionParserTests(TestCase):
    def _parse_opts(self, limit, order, **kwargs):
        args = {
            C.QK_EXPORT_LIMIT: limit,
            C.QK_EXPORT_ORDER: order,
        }
        args.update(kwargs)

        return export.parse_export_options(args)

    def test_args_without_export_options_returns_none(self):
        limit, order = export.parse_export_options({'foo': 'bar'})

        self.assertIsNone(limit)
        self.assertIsNone(order)

    def test_export_limit_without_order_by_raises_exception(self):
        with self.assertRaises(RSError) as e:
            export.parse_export_options({C.QK_EXPORT_LIMIT: '500'})

        self.assertIn(
            'export limit requires {} argument'.format(C.QK_EXPORT_ORDER),
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
        limit, order = export.parse_export_options({
            C.QK_EXPORT_LIMIT: 50,
            C.QK_EXPORT_ORDER: 'last_visit_date',
            'foo': 'bar'
        })

        self.assertEqual(limit, 50)
        self.assertEqual(order, 'last_visit_date')

    def test_export_limit_and_order_removed_from_args(self):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER: 'last_visit_date', 'foo': 'bar'}
        export.parse_export_options(args)

        self.assertEqual(args, {'foo': 'bar'})


class MetadataTests(TestCase):
    def _round_trip(self, site, cutoff, filters):
        metadata = export.create_metadata_from_parameters(site, cutoff, filters)
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
