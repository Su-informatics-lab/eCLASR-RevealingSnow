import datetime
from unittest import TestCase

from parameterized import parameterized

from snow import util


class JsonifyTests(TestCase):
    def test_jsonify_returns_string(self):
        self.assertIsInstance(util.jsonify(dict()), str)

    def test_jsonify_converts_dates_to_iso8601(self):
        data = {'key': datetime.datetime(2018, 1, 15)}
        expected = '{"key": "2018-01-15"}'
        actual = util.jsonify(data)

        self.assertEqual(actual, expected)


class ParseBooleanTests(TestCase):
    @parameterized.expand([
        (None, False),
        (False, False),
        (True, True),
        ('', False),
        ('0', False),
        ('false', False),
        ('False', False),
        ('f', False),
        ('F', False),
        ('1', True),
        ('true', True),
        ('True', True),
        ('t', True),
        ('T', True)
    ])
    def test_parse_boolean(self, value, expected):
        actual = util.parse_boolean(value)
        self.assertEqual(actual, expected)
