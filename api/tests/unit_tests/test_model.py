from unittest import TestCase

from snow import constants as C
from snow.model import CriteriaDataModel


class CriteriaDataModelTests(TestCase):
    def setUp(self):
        super(CriteriaDataModelTests, self).setUp()

        self.model = CriteriaDataModel()
        self.model._model = {
            C.FILTERS: [
                {
                    'key': 'clot',
                    'label': 'CVD',
                },
                {
                    'key': 'neuro',
                    'label': 'Neurology'
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
        }

    def test_filter_keys_returns_keys_for_all_filters(self):
        self.assertEqual(self.model.filter_keys, {'clot', 'neuro'})

    def test_site_keys_returns_keys_for_all_sites(self):
        self.assertEqual(self.model.ymca_site_keys, {'ymca_fulton', 'ymca_gateway'})
