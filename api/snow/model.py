import abc
from os import path

import yaml

from snow import constants as C, exc
from snow.util import make_json_response

DEFAULT_MODEL_FILE = path.join(path.dirname(__file__), 'data', 'model.yml')


class EmrFilter(metaclass=abc.ABCMeta):
    def __init__(self, key, attributes):
        self.key = key
        self.attributes = attributes

    @abc.abstractmethod
    def validate_filter_value(self, value):
        pass


class ToggleFilter(EmrFilter):
    _VALID_FILTER_VALUES = {'0', '1'}

    def validate_filter_value(self, value):
        if not isinstance(value, dict):
            self._validate_filter_value(value)
        else:
            if 'value' not in value:
                raise exc.RSError("filter value structure must contain 'value' element")

            self._validate_filter_value(value['value'])

    def _validate_filter_value(self, value):
        if value not in self._VALID_FILTER_VALUES:
            raise exc.RSError("invalid filter value '{}'; must be one of [{}]".format(
                value, ', '.join(self._VALID_FILTER_VALUES)
            ))


_FILTER_TYPES = {
    C.FLT_TOGGLE: ToggleFilter
}


def _load_model(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _construct_filter(filter_key, filter_type, filter_attributes):
    if filter_type not in _FILTER_TYPES:
        raise exc.RSConfigError("invalid filter type: '{}'".format(filter_type))

    filter_type = _FILTER_TYPES[filter_type]
    return filter_type(filter_key, filter_attributes)


def _construct_filters(filter_data):
    def _get_filter_tuple(filter_attributes):
        filter_attributes = dict(filter_attributes)
        filter_key = filter_attributes.pop(C.FLK_KEY)
        filter_type = filter_attributes.pop(C.FLK_TYPE)

        return filter_key, filter_type, filter_attributes

    filters = dict()
    for flt in filter_data:
        fk, ft, fa = _get_filter_tuple(flt)
        filters[fk] = _construct_filter(fk, ft, fa)

    return filters


class CriteriaDataModel(object):
    def __init__(self):
        self._model = None
        self._model_filename = DEFAULT_MODEL_FILE
        self._filters = None

    def init_app(self, app):
        if C.CRITERIA_DATA_MODEL_FILE in app.config:
            self._model_filename = app.config[C.CRITERIA_DATA_MODEL_FILE]

    @property
    def model(self):
        if self._model is None:
            self._model = _load_model(self._model_filename)

        return self._model

    @property
    def filters(self):
        if self._filters is None:
            self._filters = _construct_filters(self.model[C.FILTERS])

        return self._filters

    @property
    def filter_keys(self):
        return set(self.filters.keys())

    @property
    def ymca_site_keys(self):
        return {
            site['key']
            for site in self.model[C.YMCA_SITES]
        }

    def get_filter(self, filter_key):
        return self.filters[filter_key]


cdm = CriteriaDataModel()


def get_criteria_data_model():
    return make_json_response(cdm.model)
