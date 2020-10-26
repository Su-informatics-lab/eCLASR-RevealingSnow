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
                },
                {
                    'key': 'sex',
                    'label': 'Sex',
                    'type': 'choice',
                    'allowed_values': ['M', 'F', '0', '?']
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
        self.assertEqual(self.model.filter_keys, {'sex', 'clot', 'neuro'})

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
        ('clot', model.ValueFilter),
        ('neuro', model.ValueFilter),
        ('sex', model.ChoiceFilter),
    ])
    def test_filters_instantiated_correctly(self, key, expected_type):
        filter = self.model.get_filter(key)

        self.assertIsInstance(filter, expected_type)

    def test_app_version_injected_in_version_details(self):
        from snow import __version__

        # Version details are only injected when loading from disk, so create a
        # new CDM instance and let it load the default model.
        m = model.CriteriaDataModel().model
        self.assertIn(C.VERSION_DETAILS, m)

        vd = m[C.VERSION_DETAILS]
        app_version = list(filter(lambda x: x['key'] == C.APP_VERSION_KEY, vd))

        self.assertEqual(len(app_version), 1)
        self.assertEqual(app_version[0]['version'], __version__)


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
                'type': 'date_toggle'
            },
            {
                'key': 'neuro',
                'label': 'Neurology',
                'type': 'toggle'
            },
            {
                'key': 'current_age',
                'label': 'Age',
                'type': 'range'
            },
        ]

        filters = model._construct_filters(filter_data)

        self.assertIn('clot', filters)
        self.assertIn('neuro', filters)
        self.assertIn('current_age', filters)

        self.assertIsInstance(filters['clot'], model.DateValueFilter)
        self.assertIsInstance(filters['neuro'], model.ValueFilter)
        self.assertIsInstance(filters['current_age'], model.RangeFilter)

    @parameterized.expand([
        (C.FLT_TOGGLE, model.ValueFilter),
        (C.FLT_RANGE, model.RangeFilter),
        (C.FLT_DATE_TOGGLE, model.DateValueFilter),
    ])
    def test_construct_filter_creates_filter_of_correct_type(self, filter_type, expected_type):
        filter = model._construct_filter('key', filter_type, None)
        self.assertIsInstance(filter, expected_type)


class DateValueFilterTests(TestCase):
    def setUp(self):
        super(DateValueFilterTests, self).setUp()

        self.filter = model.DateValueFilter('foo', None)

    @parameterized.expand([
        ('bar',),
        ({'value': 'bar'}),
    ])
    def test_invalid_filter_value_raises_exception(self, value):
        with self.assertRaises(RSError) as e:
            self.filter.validate_filter_value(value)

        self.assertIn('invalid filter value', str(e.exception))

    @parameterized.expand([
        ('1', 'foo == foo'),
        ({'value': '1', 'date': '2016-07-12'}, '(foo == foo and foo >= "2016-07-12")'),
        ({'value': '0', 'date': '2016-07-12'}, '(foo != foo or foo < "2016-07-12")'),
    ])
    def test_expand_filter_expression(self, value, expected):
        actual = self.filter.expand_filter_expression('foo', value)
        self.assertEqual(actual, expected)


class ValueFilterTests(TestCase):
    def setUp(self):
        super(ValueFilterTests, self).setUp()

        self.filter = model.ValueFilter('foo', None)

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
        ('0', 'foo != 1'),
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


class ChoiceFilterTests(TestCase):
    def setUp(self) -> None:
        super(ChoiceFilterTests, self).setUp()

        # Create a choice filter that allows values A, 2, and bar. We want to validate
        # that none of the logic depends on the data type.
        self.filter = model.ChoiceFilter('foo', {'allowed_values': {'A', 2, 'bar'}})

    @parameterized.expand([
        (2,),
        ('foo',),
        ('notavar',),
        ('0',),
        ('B',),
        ('A;3',),
        ('2;B',),
        ('A;2;bar;;',),
        ('A;2;bar;baz',),
    ])
    def test_invalid_filter_value_raises_exception(self, value):
        with self.assertRaises(RSError) as e:
            self.filter.validate_filter_value(value)

        self.assertIn('invalid filter value', str(e.exception))

    @parameterized.expand([
        ('A', 'foo == "A"'),
        ('2', 'foo == "2"'),
        ('bar', 'foo == "bar"'),
        ('A;2', 'foo in ("A", "2")'),
        ('A;2;bar', 'foo in ("A", "2", "bar")'),
        ('2;bar', 'foo in ("2", "bar")'),
    ])
    def test_expand_filter_expression(self, value, expected):
        actual = self.filter.expand_filter_expression('foo', value)
        self.assertEqual(actual, expected)
