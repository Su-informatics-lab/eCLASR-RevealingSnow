import datetime
from unittest import TestCase

from snow import util


class JsonifyTests(TestCase):
    def test_jsonify_returns_string(self):
        self.assertIsInstance(util.jsonify(dict()), str)

    def test_jsonify_converts_dates_to_iso8601(self):
        data = {'key': datetime.datetime(2018, 1, 15)}
        expected = '{"key": "2018-01-15"}'
        actual = util.jsonify(data)

        self.assertEqual(actual, expected)
