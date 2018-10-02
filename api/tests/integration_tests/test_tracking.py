import responses

from snow import tracking, exc
from tests.integration_tests import TestBase, TestConfig


class TrackingConfig(TestConfig):
    TRACKING_API_URL_BASE = 'http://localhost/ehr'
    TRACKING_API_EXPORT_PATH = 'export'
    TRACKING_API_AUTH_USER = 'foo'
    TRACKING_API_AUTH_PASS = 'bar'


class TrackingSystemTests(TestBase):
    def setUp(self):
        super(TrackingSystemTests, self).setUp()

        self.app = self.create_app(TrackingConfig)
        self.tracking = tracking.TrackingSystem(self.app)

    @responses.activate
    def test_export_posts_to_configured_url(self):
        responses.add(responses.POST, 'http://localhost/ehr/export')
        self.tracking.export_data(None)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, 'http://localhost/ehr/export')

    @responses.activate
    def test_export_posts_with_authorization_header(self):
        responses.add(responses.POST, 'http://localhost/ehr/export')
        self.tracking.export_data(None)

        headers = responses.calls[0].request.headers

        self.assertEqual(headers['Authorization'], 'Basic Zm9vOmJhcg==')

    @responses.activate
    def test_export_posts_with_expected_headers(self):
        responses.add(responses.POST, 'http://localhost/ehr/export')
        self.tracking.export_data(None)

        headers = responses.calls[0].request.headers
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Accept'], 'application/json')

    @responses.activate
    def test_export_posts_with_json_payload_as_body(self):
        responses.add(responses.POST, 'http://localhost/ehr/export')
        self.tracking.export_data({'foo': 'bar'})

        self.assertEqual(responses.calls[0].request.body, b'{"foo": "bar"}')

    def test_initializing_tracking_system_with_invalid_config_raises_exception(self):
        class BadConfig(TestConfig):
            pass

        with self.assertRaises(exc.RSError) as e:
            app = self.create_app(BadConfig)
            tracking.TrackingSystem(app)

        self.assertIn('missing required configuration value for tracking system integration', str(e.exception))
