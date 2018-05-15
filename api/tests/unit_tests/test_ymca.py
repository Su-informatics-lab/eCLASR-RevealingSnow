from unittest import TestCase

import pandas as pd
from parameterized import parameterized

from snow import ymca


class YmcaDistanceTests(TestCase):
    def setUp(self):
        super(YmcaDistanceTests, self).setUp()

        pscr = {
            'patient_num': [1, 2, 3, 4],
            'ymca_fulton': [2, 3, 4, 4],
            'ymca_hanes': [8, 3, 2, 5],
        }
        self.pscr = pd.DataFrame(data=pscr)

    @parameterized.expand([
        ('ymca_fulton', {2: 1, 3: 1, 4: 2}),
        ('ymca_hanes', {2: 1, 3: 1, 5: 1, 8: 1}),
    ])
    def test_site_distance_without_cutoff(self, site, expected):
        actual = ymca.get_ymca_distance_stats(self.pscr, site)
        self.assertEqual(actual, {site: expected})

    @parameterized.expand([
        ('ymca_fulton', 4, {2: 1, 3: 1}),
        ('ymca_hanes', 4, {2: 1, 3: 1}),
    ])
    def test_site_distance_with_cutoff(self, site, cutoff, expected):
        actual = ymca.get_ymca_distance_stats(self.pscr, site, cutoff=cutoff)

        self.assertEqual(actual, {site: expected})
