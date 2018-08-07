from unittest import TestCase

import yaml

from snow import constants as C
from snow import query
from snow.exc import RSError


class QueryArgParserTests(TestCase):
    def test_empty_query_unchanged(self):
        result = query.parse_query_args(dict())
        self.assertEqual(result, dict())

    def test_simple_argument_unchanged(self):
        q = {'foo': 'bar'}
        result = query.parse_query_args(q)
        self.assertEqual(result, q)

    def test_dot_notation_converted_to_nested_dict(self):
        result = query.parse_query_args({'foo.bar': 'baz'})
        self.assertEqual(result, {'foo': {'bar': 'baz'}})

    def test_multiple_dot_notation_merged_in_nested(self):
        result = query.parse_query_args({'foo.bar': 'baz', 'foo.baz': 'qux'})
        self.assertEqual(result, {'foo': {'bar': 'baz', 'baz': 'qux'}})

    def test_multilevel_dot_notation_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_query_args({'foo.bar.baz': '1'})

        self.assertIn("multi-level query args are not supported", str(e.exception))

    def test_field_with_both_simple_argument_and_dot_notation_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_query_args({
                'foo': 'bar',
                'foo.bar': 'baz'
            })

        self.assertIn(
            'field(s) cannot have both simple value and nested value',
            str(e.exception)
        )


class YmcaQueryArgParserTests(TestCase):
    def test_query_without_site_argument_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args(dict())

        self.assertIn("missing required argument: 'site'", str(e.exception))

    def test_query_with_invalid_site_argument_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args({'site': 'foobar', 'cutoff': '5'})

        self.assertIn("invalid YMCA site: 'foobar'", str(e.exception))

    def test_query_with_only_site_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args({'site': 'ymca_fulton'})

        self.assertIn("missing required argument: 'cutoff'", str(e.exception))

    def test_query_with_cutoff(self):
        site, cutoff, filters = query.parse_ymca_query_args({'site': 'ymca_fulton', 'cutoff': '5'})
        self.assertEqual(site, ['ymca_fulton'])
        self.assertEqual(cutoff, [5])
        self.assertEqual(filters, dict())

    def test_query_with_cutoff_and_filters(self):
        site, cutoff, filters = query.parse_ymca_query_args({
            'site': 'ymca_fulton',
            'sex': 'M',
            'cutoff': '5'
        })

        self.assertEqual(site, ['ymca_fulton'])
        self.assertEqual(cutoff, [5])
        self.assertEqual(filters, {'sex': 'M'})

    def test_query_with_multiple_sites(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args({'site': 'ymca_fulton,ymca_davie'})

        self.assertIn("missing required argument: 'cutoff'", str(e.exception))

    def test_query_with_multiple_sites_and_single_cutoff_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args({'site': 'ymca_fulton,ymca_davie', 'cutoff': '5'})

        self.assertIn(
            'number of YMCA sites (2) must match number of cutoffs (1)',
            str(e.exception)
        )

    def test_query_with_single_site_and_multiple_cutoffs_raises_exception(self):
        with self.assertRaises(RSError) as e:
            query.parse_ymca_query_args({'site': 'ymca_fulton', 'cutoff': '5,10'})

        self.assertIn(
            'number of YMCA sites (1) must match number of cutoffs (2)',
            str(e.exception)
        )

    def test_query_with_multiple_sites_and_cutoffs(self):
        site, cutoff, filters = query.parse_ymca_query_args({
            'site': 'ymca_fulton,ymca_davie',
            'cutoff': '5,10'
        })

        self.assertEqual(site, ['ymca_fulton', 'ymca_davie'])
        self.assertEqual(cutoff, [5, 10])
        self.assertEqual(filters, dict())


class MetadataTests(TestCase):
    def _round_trip(self, site, cutoff, filters):
        metadata = query.create_metadata_from_parameters(site, cutoff, filters)
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
