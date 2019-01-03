import responses

from snow import constants as C
from snow import tracking, exc
from tests.integration_tests import TestBase, TestConfig


class TrackingConfig(TestConfig):
    TRACKING_API_ENABLED = True
    TRACKING_API_URL_BASE = 'http://localhost/ehr'
    TRACKING_API_EXPORT_PATH = 'export'
    TRACKING_API_AUTH_USER = 'foo'
    TRACKING_API_AUTH_PASS = 'bar'


class TrackingSystemTests(TestBase):
    def setUp(self):
        super(TrackingSystemTests, self).setUp()

        self.app = self.create_app(TrackingConfig)
        self.tracking = tracking.TrackingSystem(self.app)

    def test_initializing_tracking_system_with_invalid_config_raises_exception(self):
        class BadConfig(TestConfig):
            TRACKING_API_ENABLED = True

        with self.assertRaises(exc.RSConfigError) as e:
            app = self.create_app(BadConfig)
            tracking.TrackingSystem(app)

        self.assertIn('missing required configuration value for tracking system integration', str(e.exception))

    def test_initializing_tracking_system_with_disabled_raises_exception_upon_export_request(self):
        class DisabledConfig(TestConfig):
            TRACKING_API_ENABLED = False

        app = self.create_app(DisabledConfig)
        track = tracking.TrackingSystem(app)

        with self.assertRaises(exc.RSConfigError) as e:
            track.export_data(None)

        self.assertIn('export_data cannot be used when {} is False'.format(C.TRACKING_API_ENABLED), str(e.exception))

    def _prepare_valid_response(self):
        responses.add(responses.POST, 'http://localhost/ehr/export', json='')

    @responses.activate
    def test_export_posts_to_configured_url(self):
        self._prepare_valid_response()
        self.tracking.export_data(None)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, 'http://localhost/ehr/export')

    @responses.activate
    def test_export_posts_with_authorization_header(self):
        self._prepare_valid_response()
        self.tracking.export_data(None)

        headers = responses.calls[0].request.headers

        self.assertEqual(headers['Authorization'], 'Basic Zm9vOmJhcg==')

    @responses.activate
    def test_export_posts_with_expected_headers(self):
        self._prepare_valid_response()
        self.tracking.export_data(None)

        headers = responses.calls[0].request.headers
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Accept'], 'application/json')

    @responses.activate
    def test_export_posts_with_json_payload_as_body(self):
        self._prepare_valid_response()
        self.tracking.export_data({'foo': 'bar'})

        self.assertEqual(responses.calls[0].request.body, b'{"foo": "bar"}')

    @responses.activate
    def test_export_reponse_with_non_json_body_raises_exception(self):
        responses.add(responses.POST, 'http://localhost/ehr/export', body='foobar')

        with self.assertRaises(exc.RSExportError) as e:
            self.tracking.export_data({'foo': 'bar'})

        self.assertIn('export to tracking failed: expected JSON response from remote API', str(e.exception))

    @responses.activate
    def test_export_reponse_returns_json_body(self):
        responses.add(responses.POST, 'http://localhost/ehr/export', json='foobar')

        response = self.tracking.export_data({'foo': 'bar'})
        self.assertEqual(response, 'foobar')

    @responses.activate
    def test_export_status_not_200_raises_exception(self):
        responses.add(responses.POST, 'http://localhost/ehr/export', json='foobar', status=400)

        with self.assertRaises(exc.RSExportError) as e:
            self.tracking.export_data({'foo': 'bar'})

        self.assertIn('export to tracking failed: unexpected status code', str(e.exception))
