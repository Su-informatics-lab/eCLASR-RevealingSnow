import requests
from requests import auth

from snow import constants as C, exc


def _get_required_value(app, key):
    value = app.config.get(key)

    if value is None:
        raise exc.RSError(
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

        self._export_url = '/'.join([self.url_base, self.export_path])
        self._auth = auth.HTTPBasicAuth(self.auth_user, self.auth_pass)

    def _post(self, url, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        return requests.post(url, json=payload, headers=headers, auth=self._auth)

    def export_data(self, payload):
        return self._post(self._export_url, payload)
