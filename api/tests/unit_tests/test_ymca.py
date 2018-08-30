from unittest import TestCase

import pandas as pd
from parameterized import parameterized

import snow.constants as C
from snow import ymca
from snow.exc import RSError
from snow.ymca import SiteMode


class YmcaDistanceTests(TestCase):
    def setUp(self):
        super(YmcaDistanceTests, self).setUp()

        pscr = {
            'patient_num': [1, 2, 3, 4],
            C.COL_SEX: ['M', 'F', 'M', 'F'],
            C.COL_RACE: ['W', 'W', 'B', 'B'],
            C.COL_ETHNICITY: ['N', 'U', 'U', 'N'],
            'ymca_fulton': [2, 3, 4, 4],
            'ymca_hanes': [8, 3, 2, 5],
        }
        self.pscr = pd.DataFrame(data=pscr)

    def test_get_ymca_distance_stats_with_multiple_sites_raises_exception(self):
        with self.assertRaises(RSError) as e:
            ymca.get_ymca_distance_stats(self.pscr, ['ymca_fulton', 'ymca_hanes'], cutoffs=[1, 2])

        self.assertIn('get_ymca_distance_stats does not support multiple sites', str(e.exception))

    @parameterized.expand([
        ('ymca_fulton', {2: 1, 3: 1, 4: 2}),
        ('ymca_hanes', {2: 1, 3: 1, 5: 1, 8: 1}),
    ])
    def test_site_distance_without_cutoff(self, site, expected):
        actual = ymca._get_distance_counts(self.pscr, site)
        self.assertEqual(actual, {site: expected})

    @parameterized.expand([
        ('ymca_fulton', 4, {2: 1, 3: 1}),
        ('ymca_hanes', 4, {2: 1, 3: 1}),
    ])
    def test_site_distance_with_cutoff(self, site, cutoff, expected):
        actual = ymca.get_ymca_distance_stats(self.pscr, [site], cutoffs=[cutoff])

        self.assertEqual(actual, {site: expected})

    def test_filter_multiple_sites_with_all_mode(self):
        actual = ymca.filter_by_distance(
            self.pscr,
            sites=['ymca_fulton', 'ymca_hanes'],
            cutoffs=[4, 4],
            mode=SiteMode.ALL
        )

        self.assertEqual(set(actual.patient_num), {2})

    def test_filter_multiple_sites_with_any_mode(self):
        actual = ymca.filter_by_distance(
            self.pscr,
            sites=['ymca_fulton', 'ymca_hanes'],
            cutoffs=[4, 4],
            mode=SiteMode.ANY
        )

        self.assertEqual(set(actual.patient_num), {1, 2, 3})

    @parameterized.expand([
        (C.COL_SEX, {'M': {2: 1, 4: 1}, 'F': {3: 1, 4: 1}}),
        (C.COL_RACE, {'W': {2: 1, 3: 1}, 'B': {4: 2}}),
        (C.COL_ETHNICITY, {'N': {2: 1, 4: 1}, 'U': {3: 1, 4: 1}}),
    ])
    def test_site_distance_with_categories(self, category, expected):
        stats = ymca.get_ymca_distance_stats(self.pscr, ['ymca_fulton'], [10], categories=[category])
        self.assertIn('ymca_fulton', stats)

        stats = stats['ymca_fulton']
        self.assertIn(C.RK_TOTAL, stats)
        self.assertIn(category, stats)

        self.assertEqual(stats[category], expected)
