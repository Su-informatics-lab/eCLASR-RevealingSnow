import json
import logging

import requests
from requests import auth

from snow import constants as C, exc

logger = logging.getLogger(__name__)


def _get_required_value(app, key):
    value = app.config.get(key)

    if value is None:
        raise exc.RSConfigError(
            "missing required configuration value for tracking system integration: '{}'".format(key)
        )

    return value


class TrackingSystem(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    # noinspection PyAttributeOutsideInit
    def init_app(self, app):
        self.url_base = _get_required_value(app, C.TRACKING_API_URL_BASE)
        self.export_path = _get_required_value(app, C.TRACKING_API_EXPORT_PATH)
        self.auth_user = _get_required_value(app, C.TRACKING_API_AUTH_USER)
        self.auth_pass = _get_required_value(app, C.TRACKING_API_AUTH_PASS)
        self.timeout = _get_required_value(app, C.TRACKING_API_TIMEOUT)

        self._export_url = '/'.join([self.url_base, self.export_path])
        self._auth = auth.HTTPBasicAuth(self.auth_user, self.auth_pass)

    def _post(self, url, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        return requests.post(url, json=payload, headers=headers, auth=self._auth, timeout=self.timeout)

    def export_data(self, payload):
        response = self._post(self._export_url, payload)

        if response.status_code != 200:
            logger.warning(
                "request to '%s' returned unexpected response: response body='%s', headers=%s",
                self._export_url, response.text, response.headers
            )

            raise exc.RSExportError("export to tracking failed: unexpected status code {}".format(response.status_code))

        try:
            return response.json()
        except json.JSONDecodeError:
            raise exc.RSExportError(
                "export to tracking failed: expected JSON response from remote API, got: '{}'".format(response.content)
            )


tracking = TrackingSystem()
