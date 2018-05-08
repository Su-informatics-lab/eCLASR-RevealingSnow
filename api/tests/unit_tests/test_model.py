from unittest import TestCase

from snow.model import CriteriaDataModel


class CriteriaDataModelTests(TestCase):
    def setUp(self):
        super(CriteriaDataModelTests, self).setUp()

        self.model = CriteriaDataModel()
        self.model._model = {
            'filters': [
                {
                    'key': 'clot',
                    'label': 'CVD',
                },
                {
                    'key': 'neuro',
                    'label': 'Neurology'
                }
            ]
        }

    def test_filter_keys_returns_keys_for_all_filters(self):
        self.assertEqual(self.model.filter_keys, {'clot', 'neuro'})
