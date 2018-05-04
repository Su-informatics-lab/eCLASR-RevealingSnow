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
