from unittest import TestCase

from parameterized import parameterized

from snow import constants as C
from snow import request
from snow.exc import RSError


class SimplifyQueryArgTests(TestCase):
    def test_empty_query_unchanged(self):
        result = request.simplify_query_args(dict())
        self.assertEqual(result, dict())

    def test_simple_argument_unchanged(self):
        q = {'foo': 'bar'}
        result = request.simplify_query_args(q)
        self.assertEqual(result, q)

    def test_dot_notation_converted_to_nested_dict(self):
        result = request.simplify_query_args({'foo.bar': 'baz'})
        self.assertEqual(result, {'foo': {'bar': 'baz'}})

    def test_multiple_dot_notation_merged_in_nested(self):
        result = request.simplify_query_args({'foo.bar': 'baz', 'foo.baz': 'qux'})
        self.assertEqual(result, {'foo': {'bar': 'baz', 'baz': 'qux'}})

    def test_multilevel_dot_notation_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.simplify_query_args({'foo.bar.baz': '1'})

        self.assertIn("multi-level query args are not supported", str(e.exception))

    def test_field_with_both_simple_argument_and_dot_notation_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.simplify_query_args({
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
            request.parse_ymca_query_args(dict())

        self.assertIn("missing required argument: 'site'", str(e.exception))

    def test_query_with_invalid_site_argument_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.parse_ymca_query_args({'site': 'foobar', 'cutoff': '5'})

        self.assertIn("invalid YMCA site: 'foobar'", str(e.exception))

    def test_query_with_only_site_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.parse_ymca_query_args({'site': 'ymca_fulton'})

        self.assertIn("missing required argument: 'cutoff'", str(e.exception))

    def test_query_with_cutoff(self):
        site, cutoff, filters = request.parse_ymca_query_args({'site': 'ymca_fulton', 'cutoff': '5'})
        self.assertEqual(site, ['ymca_fulton'])
        self.assertEqual(cutoff, [5])
        self.assertEqual(filters, dict())

    def test_query_with_cutoff_and_filters(self):
        site, cutoff, filters = request.parse_ymca_query_args({
            'site': 'ymca_fulton',
            'sex': 'M',
            'cutoff': '5'
        })

        self.assertEqual(site, ['ymca_fulton'])
        self.assertEqual(cutoff, [5])
        self.assertEqual(filters, {'sex': 'M'})

    def test_query_with_multiple_sites(self):
        with self.assertRaises(RSError) as e:
            request.parse_ymca_query_args({'site': 'ymca_fulton,ymca_davie'})

        self.assertIn("missing required argument: 'cutoff'", str(e.exception))

    def test_query_with_multiple_sites_and_single_cutoff_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.parse_ymca_query_args({'site': 'ymca_fulton,ymca_davie', 'cutoff': '5'})

        self.assertIn(
            'number of YMCA sites (2) must match number of cutoffs (1)',
            str(e.exception)
        )

    def test_query_with_single_site_and_multiple_cutoffs_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.parse_ymca_query_args({'site': 'ymca_fulton', 'cutoff': '5,10'})

        self.assertIn(
            'number of YMCA sites (1) must match number of cutoffs (2)',
            str(e.exception)
        )

    def test_query_with_multiple_sites_and_cutoffs(self):
        site, cutoff, filters = request.parse_ymca_query_args({
            'site': 'ymca_fulton,ymca_davie',
            'cutoff': '5,10'
        })

        self.assertEqual(site, ['ymca_fulton', 'ymca_davie'])
        self.assertEqual(cutoff, [5, 10])
        self.assertEqual(filters, dict())


class ParseExportLimitTests(TestCase):
    def _parse_opts(self, limit, order, **kwargs):
        args = {
            C.QK_EXPORT_LIMIT: limit,
            C.QK_EXPORT_ORDER_BY: order,
        }
        args.update(kwargs)

        return request.parse_limit_arguments(args)

    def test_args_without_export_options_returns_none(self):
        limits = request.parse_limit_arguments({'foo': 'bar'})

        self.assertIsNone(limits.limit)
        self.assertIsNone(limits.order_by)

    def test_export_limit_without_order_by_raises_exception(self):
        with self.assertRaises(RSError) as e:
            request.parse_limit_arguments({C.QK_EXPORT_LIMIT: '500'})

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
            self._parse_opts('foobar', C.QK_LIMIT_LAST_VISIT_DATE)

        self.assertIn('invalid export limit', str(e.exception))

    def test_export_limit_and_order_returned(self):
        limits = request.parse_limit_arguments({
            C.QK_EXPORT_LIMIT: 50,
            C.QK_EXPORT_ORDER_BY: C.QK_LIMIT_LAST_VISIT_DATE,
            'foo': 'bar'
        })

        self.assertEqual(limits.limit, 50)
        self.assertEqual(limits.order_by, C.QK_LIMIT_LAST_VISIT_DATE)

    def test_export_limit_and_order_removed_from_args(self):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: C.QK_LIMIT_LAST_VISIT_DATE, 'foo': 'bar'}
        request.parse_limit_arguments(args)

        self.assertEqual(args, {'foo': 'bar'})

    def test_order_asc_defaults_to_false(self):
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: C.QK_LIMIT_LAST_VISIT_DATE}
        limits = request.parse_limit_arguments(args)

        self.assertFalse(limits.order_asc)

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
        args = {C.QK_EXPORT_LIMIT: 50, C.QK_EXPORT_ORDER_BY: C.QK_LIMIT_LAST_VISIT_DATE,
            C.QK_EXPORT_ORDER_ASC: order_asc}
        limits = request.parse_limit_arguments(args)

        self.assertEqual(limits.order_asc, expected)
