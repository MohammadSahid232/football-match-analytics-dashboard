"""
test_fifa2026_eda.py
Unit tests for the FIFA 2026 Exploratory Data Analysis services.
"""

import unittest
import pandas as pd
from app.services.fifa2026_eda import (
    get_tournament_summary, get_top_scorers, get_top_assisters,
    goals_by_round, goals_by_confederation, attendance_summary,
    correlation_matrix, host_nation_analysis, red_yellow_analysis
)


class TestFIFA2026EDA(unittest.TestCase):

    def test_get_tournament_summary(self):
        summary = get_tournament_summary()
        self.assertIsInstance(summary, dict)
        # Check mandatory summary keys
        keys = ['total_matches', 'total_goals', 'avg_goals_per_match',
                'highest_match_goals', 'draws', 'highest_scoring_match',
                'top_scorer', 'total_yellow_cards', 'total_red_cards', 'avg_attendance']
        for key in keys:
            self.assertIn(key, summary)
            
        self.assertEqual(summary['total_matches'], 104)
        self.assertTrue(summary['total_goals'] > 0)
        self.assertTrue(summary['avg_goals_per_match'] > 0)

    def test_get_top_scorers(self):
        df_scorers = get_top_scorers(5)
        self.assertIsInstance(df_scorers, pd.DataFrame)
        self.assertEqual(len(df_scorers), 5)
        self.assertIn('Goals', df_scorers.columns)
        # Ensure it is sorted descending by goals
        goals_list = df_scorers['Goals'].tolist()
        self.assertEqual(goals_list, sorted(goals_list, reverse=True))

    def test_get_top_assisters(self):
        df_assisters = get_top_assisters(5)
        self.assertIsInstance(df_assisters, pd.DataFrame)
        self.assertEqual(len(df_assisters), 5)
        self.assertIn('Assists', df_assisters.columns)
        # Ensure it is sorted descending by assists
        assists_list = df_assisters['Assists'].tolist()
        self.assertEqual(assists_list, sorted(assists_list, reverse=True))

    def test_goals_by_round(self):
        series = goals_by_round()
        self.assertIsInstance(series, pd.Series)
        self.assertFalse(series.empty)
        # Verify specific rounds exist in output
        self.assertIn('Group Stage', series.index)
        self.assertIn('Final', series.index)

    def test_goals_by_confederation(self):
        series = goals_by_confederation()
        self.assertIsInstance(series, pd.Series)
        self.assertFalse(series.empty)
        # E.g., CONCACAF or UEFA should be present
        self.assertTrue(any(c in series.index for c in ['UEFA', 'CONMEBOL', 'CONACAF', 'CONCACAF']))

    def test_attendance_summary(self):
        df_att = attendance_summary()
        self.assertIsInstance(df_att, pd.DataFrame)
        self.assertIn('Avg_Attendance', df_att.columns)
        self.assertIn('Venue', df_att.columns)
        self.assertTrue(len(df_att) > 0)

    def test_correlation_matrix(self):
        df_corr = correlation_matrix()
        self.assertIsInstance(df_corr, pd.DataFrame)
        # Check that it's a square matrix
        self.assertEqual(df_corr.shape[0], df_corr.shape[1])
        # Values must be within [-1, 1] bounds
        self.assertTrue((df_corr.dropna().values >= -1.0).all())
        self.assertTrue((df_corr.dropna().values <= 1.0).all())

    def test_host_nation_analysis(self):
        host_analysis = host_nation_analysis()
        self.assertIsInstance(host_analysis, dict)
        self.assertIn('host_match_count', host_analysis)
        self.assertIn('host_avg_goals', host_analysis)
        self.assertTrue(host_analysis['host_match_count'] > 0)

    def test_red_yellow_analysis(self):
        card_analysis = red_yellow_analysis()
        self.assertIsInstance(card_analysis, dict)
        self.assertIn('total_yellow_cards', card_analysis)
        self.assertIn('total_red_cards', card_analysis)
        self.assertIn('avg_yellow_per_match', card_analysis)


if __name__ == '__main__':
    unittest.main()
