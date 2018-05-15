from unittest import TestCase

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
            query.parse_ymca_query_args({'site': 'foobar'})

        self.assertIn("invalid YMCA site: 'foobar'", str(e.exception))

    def test_query_with_only_site(self):
        site, cutoff, filters = query.parse_ymca_query_args({'site': 'ymca_fulton'})

        self.assertEqual(site, 'ymca_fulton')
        self.assertIsNone(cutoff)
        self.assertEqual(filters, dict())

    def test_query_with_cutoff(self):
        site, cutoff, filters = query.parse_ymca_query_args({'site': 'ymca_fulton', 'cutoff': '5'})
        self.assertEqual(site, 'ymca_fulton')
        self.assertEqual(cutoff, 5)
        self.assertEqual(filters, dict())

    def test_query_with_filters(self):
        site, cutoff, filters = query.parse_ymca_query_args({'site': 'ymca_fulton', 'sex': 'M'})
        self.assertEqual(site, 'ymca_fulton')
        self.assertIsNone(cutoff)
        self.assertEqual(filters, {'sex': 'M'})

    def test_query_with_cutoff_and_filters(self):
        site, cutoff, filters = query.parse_ymca_query_args({
            'site': 'ymca_fulton',
            'sex': 'M',
            'cutoff': '5'
        })

        self.assertEqual(site, 'ymca_fulton')
        self.assertEqual(cutoff, 5)
        self.assertEqual(filters, {'sex': 'M'})
