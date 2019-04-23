from unittest import TestCase

from parameterized import parameterized

from snow import constants as C, exc
from snow import model
from snow.exc import RSError


def create_model(props):
    m = model.CriteriaDataModel()
    m._model = props

    return m


class CriteriaDataModelTests(TestCase):
    def setUp(self):
        super(CriteriaDataModelTests, self).setUp()

        self.model = create_model({
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
        })

    def test_filter_keys_returns_keys_for_all_filters(self):
        self.assertEqual(self.model.filter_keys, {'clot', 'neuro'})

    def test_site_keys_returns_keys_for_all_sites(self):
        self.assertEqual(self.model.ymca_site_keys, {'ymca_fulton', 'ymca_gateway'})

    def test_data_version_is_none_when_undefined(self):
        self.assertIsNone(self.model.data_version)

    def test_data_version(self):
        props = dict(self.model._model)
        props[C.DATA_VERSION] = '12345'
        model = create_model(props)

        self.assertEqual(model.data_version, '12345')

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

    @parameterized.expand([
        ('toggle', model.ToggleFilter),
        ('range', model.RangeFilter),
    ])
    def test_construct_filter_creates_filter_of_correct_type(self, filter_type, expected_type):
        filter = model._construct_filter('key', filter_type, None)
        self.assertIsInstance(filter, expected_type)


class ToggleFilterTests(TestCase):
    def setUp(self):
        super(ToggleFilterTests, self).setUp()

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
        ('1', 'foo == 1'),
        ({'value': '1', 'date': '2016-07-12'}, '(foo == 1 and foo_date >= "2016-07-12")'),
        ({'value': '0', 'date': '2016-07-12'}, '(foo == 0 or foo_date < "2016-07-12")'),
    ])
    def test_expand_filter_expression(self, value, expected):
        actual = self.filter.expand_filter_expression('foo', value)
        self.assertEqual(actual, expected)


class RangeFilterTests(TestCase):
    def setUp(self):
        super(RangeFilterTests, self).setUp()

        self.filter = model.RangeFilter('foo', None)

    @parameterized.expand([
        ('bar',),
        ('1',),
        ({'value': '1'},),
        ({'min': '10', 'max': '1'},)
    ])
    def test_invalid_filter_value_raises_exception(self, value):
        with self.assertRaises(RSError) as e:
            self.filter.validate_filter_value(value)

        self.assertIn('invalid filter value', str(e.exception))

    @parameterized.expand([
        ({'min': '1'}, 'foo >= 1.0'),
        ({'min': '2.5'}, 'foo >= 2.5'),
        ({'max': '10'}, 'foo <= 10.0'),
        ({'min': '1.25', 'max': '9.75'}, '(foo >= 1.25 and foo <= 9.75)'),
    ])
    def test_expand_filter_expression(self, value, expected):
        actual = self.filter.expand_filter_expression('foo', value)
        self.assertEqual(actual, expected)
