from os import path

import yaml

from snow import constants as C
from snow.util import make_json_response

DEFAULT_MODEL_FILE = path.join(path.dirname(__file__), 'data', 'model.yml')


def _load_model(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


class CriteriaDataModel(object):
    def __init__(self):
        self._model = None
        self._model_filename = DEFAULT_MODEL_FILE

    def init_app(self, app):
        if C.CRITERIA_DATA_MODEL_FILE in app.config:
            self._model_filename = app.config[C.CRITERIA_DATA_MODEL_FILE]

    @property
    def model(self):
        if self._model is None:
            self._model = _load_model(self._model_filename)

        return self._model

    @property
    def filter_keys(self):
        return {
            filter['key']
            for filter in self.model['filters']
        }


cdm = CriteriaDataModel()


def get_criteria_data_model():
    return make_json_response(cdm.model)
