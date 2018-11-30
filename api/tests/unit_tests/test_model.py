from unittest import TestCase

from parameterized import parameterized

from snow import constants as C, exc
from snow import model
from snow.exc import RSError


class CriteriaDataModelTests(TestCase):
    def setUp(self):
        super(CriteriaDataModelTests, self).setUp()

        self.model = model.CriteriaDataModel()
        self.model._model = {
            C.FILTERS: [
                {
                    'key': 'clot',
                    'label': 'CVD',
                    'type': 'toggle'
                },
                {
                    'key': 'neuro',
                    'label': 'Neurology',
                    'type': 'toggle'
                }
            ],
            C.YMCA_SITES: [
                {
                    'key': 'ymca_fulton',
                    'label': 'Fulton',
                },
                {
                    'key': 'ymca_gateway',
                    'label': 'Gateway',
                },
            ],
        }

    def test_filter_keys_returns_keys_for_all_filters(self):
        self.assertEqual(self.model.filter_keys, {'clot', 'neuro'})

    def test_site_keys_returns_keys_for_all_sites(self):
        self.assertEqual(self.model.ymca_site_keys, {'ymca_fulton', 'ymca_gateway'})

    @parameterized.expand([
        ('clot', model.ToggleFilter),
        ('neuro', model.ToggleFilter),
    ])
    def test_filters_instantiated_correctly(self, key, expected_type):
        filter = self.model.get_filter(key)
        self.assertIsInstance(filter, expected_type)


class ModelHelperFunctionTests(TestCase):
    def test_invalid_filter_type_raises_exception(self):
        with self.assertRaises(exc.RSConfigError) as e:
            model._construct_filter('foo', 'bar', None)

        self.assertIn('invalid filter type', str(e.exception))

    def test_construct_filters_creates_dictionary_of_filter_objects(self):
        filter_data = [
            {
                'key': 'clot',
                'label': 'CVD',
                'type': 'toggle'
            },
            {
                'key': 'neuro',
                'label': 'Neurology',
                'type': 'toggle'
            }
        ]

        filters = model._construct_filters(filter_data)

        self.assertIn('clot', filters)
        self.assertIn('neuro', filters)

        self.assertIsInstance(filters['clot'], model.ToggleFilter)
        self.assertIsInstance(filters['neuro'], model.ToggleFilter)


class ToggleFilterTests(TestCase):
    def setUp(self):
        self.filter = model.ToggleFilter('foo', None)

    @parameterized.expand([
        ('bar',),
        ({'value': 'bar'}),
    ])
    def test_invalid_filter_value_raises_exception(self, value):
        with self.assertRaises(RSError) as e:
            self.filter.validate_filter_value(value)

        self.assertIn('invalid filter value', str(e.exception))

    @parameterized.expand([
        ('foo', '1', 'foo == 1'),
        ('foo', {'value': '1', 'date': '2016-07-12'}, '(foo == 1 and foo_date >= "2016-07-12")'),
        ('foo', {'value': '0', 'date': '2016-07-12'}, '(foo == 0 or foo_date < "2016-07-12")'),
    ])
    def test_expand_filter_expression(self, key, value, expected):
        actual = self.filter.expand_filter_expression(key, value)
        self.assertEqual(actual, expected)
