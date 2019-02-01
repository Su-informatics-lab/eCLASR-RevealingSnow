import re
from unittest import TestCase

import pandas as pd

from snow import constants as C, request
from snow import export
from snow.exc import RSError

TEST_DATA_VERSION = '12345'


class ExportOptionTests(TestCase):
    def _create_metadata(self, site, maxdist, filters, limit=None, order_by=None, order_asc=None, **kwargs):
        query = request.Query(
            request.FilterArguments(filters),
            request.SiteArguments(site, maxdist),
            request.LimitArguments(limit, order_by, order_asc)
        )

        opts = export.ExportOptions(query, **kwargs)

        return opts.create_metadata()

    def test_empty_metadata(self):
        actual = self._create_metadata(None, None, None)
        self.assertEqual(actual, {C.FILTERS: None})

    def test_metadata_includes_data_version_when_defined(self):
        actual = self._create_metadata(None, None, None, data_version=TEST_DATA_VERSION)
        self.assertEqual(actual, {C.FILTERS: None, C.DATA_VERSION: TEST_DATA_VERSION})

    def test_metadata_from_sites_only_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._create_metadata(['ymca_hanes'], None, None)

        self.assertIn('sites and maxdists must both be present or both be None', str(e.exception))

    def test_metadata_from_maxdists_only_raises_exception(self):
        with self.assertRaises(RSError) as e:
            self._create_metadata(None, [5], None)

        self.assertIn('sites and maxdists must both be present or both be None', str(e.exception))

    def test_metadata_from_sites_and_maxdists(self):
        expected = {
            C.YMCA_SITES: {
                'ymca_fulton': 5,
                'ymca_davie': 10
            },
            C.FILTERS: None
        }

        actual = self._create_metadata(['ymca_fulton', 'ymca_davie'], [5, 10], None)

        self.assertEqual(actual, expected)

    def test_metadata_from_filters(self):
        filters = {'hospice': '0', 'bariatric': {
            'value': '1',
            'date': '2018-01-01'
        }}

        expected = {
            C.FILTERS: filters
        }

        actual = self._create_metadata(None, None, filters)

        self.assertEqual(actual, expected)

    def test_metadata_from_sites_maxdists_and_filters(self):
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

        actual = self._create_metadata(['ymca_fulton', 'ymca_davie'], [5, 10], filters)

        self.assertEqual(actual, expected)

    def test_metadata_with_limit(self):
        expected = {
            C.FILTERS: None,
            C.PATIENT_SUBSET: {
                C.QK_EXPORT_LIMIT: 50,
                C.QK_EXPORT_ORDER_BY: 'foo',
                C.QK_EXPORT_ORDER_ASC: True
            }
        }

        actual = self._create_metadata(None, None, None, 50, 'foo', True)

        self.assertEqual(actual, expected)

    def test_metadata_with_label(self):
        expected = {
            C.FILTERS: None,
            C.EXPORT_LABEL: 'foobar'
        }

        actual = self._create_metadata(None, None, None, label='foobar')

        self.assertEqual(actual, expected)

    def test_metadata_with_description(self):
        expected = {
            C.FILTERS: None,
            C.EXPORT_DESCRIPTION: 'foobar'
        }

        actual = self._create_metadata(None, None, None, description='foobar')

        self.assertEqual(actual, expected)

    def test_user_in_metadata(self):
        expected = {
            C.FILTERS: None,
            C.EXPORT_USER: 'foobar'
        }

        actual = self._create_metadata(None, None, None, userid='foobar')

        self.assertEqual(actual, expected)


class ExportDataTests(TestCase):
    def setUp(self):
        super(ExportDataTests, self).setUp()

        self.opts = export.ExportOptions(None, None, None, None)
        self.subj = pd.DataFrame(data={'patient_num': [1, 2, 3]})

    def _create_export_data(self, **kwargs):
        return export.ExportData(self.opts, self.subj, **kwargs)

    def test_export_data_constructor_sets_identifier_when_absent(self):
        data = self._create_export_data()

        self.assertIsNotNone(data.identifier)
        self.assertTrue(re.match(r'[0-9a-fA-F-]{36}', data.identifier))

    def test_export_data_constructor_sets_timestamp_when_absent(self):
        data = self._create_export_data()

        self.assertIsNotNone(data.timestamp)
        self.assertTrue(re.match(r'[0-9]{10}', data.timestamp))

    def test_export_data_uses_provided_identifier(self):
        data = self._create_export_data(identifier='foobar')

        self.assertEqual(data.identifier, 'foobar')

    def test_export_data_uses_provided_timestamp(self):
        data = self._create_export_data(timestamp='foobar')

        self.assertEqual(data.timestamp, 'foobar')

    def test_export_data_flags_have_expected_values(self):
        data = self._create_export_data()

        self.assertEqual(data.flags, C.EP_FLAG_VALUES)

    def test_export_payload_structured_as_expected(self):
        data = self._create_export_data()
        payload = data.create_export_payload()

        print(payload)

        self.assertIn(C.EP_ID, payload)
        self.assertIn(C.EP_TS, payload)
        self.assertIn(C.EP_SUBJECTS, payload)
        self.assertIn(C.EP_METADATA, payload)
        self.assertIn(C.EP_FLAGS, payload)

        self.assertIsInstance(payload[C.EP_ID], str)
        self.assertIsInstance(payload[C.EP_TS], str)
        self.assertIsInstance(payload[C.EP_SUBJECTS], list)
        self.assertIsInstance(payload[C.EP_METADATA], dict)
        self.assertIsInstance(payload[C.EP_FLAGS], dict)


class ParseExportQueryTests(TestCase):
    def setUp(self):
        pass

    def test_export_label(self):
        label, description, user = export.parse_export_identifiers({C.EXPORT_LABEL: 'foo'})

        self.assertEqual(label, 'foo')
        self.assertIsNone(description)
        self.assertIsNone(user)

    def test_export_description(self):
        label, description, user = export.parse_export_identifiers({C.EXPORT_DESCRIPTION: 'foo'})

        self.assertIsNone(label)
        self.assertEqual(description, 'foo')
        self.assertIsNone(user)

    def test_export_userid(self):
        label, description, user = export.parse_export_identifiers({C.EXPORT_USER: 'foo'})

        self.assertIsNone(label)
        self.assertIsNone(description)
        self.assertEqual(user, 'foo')
