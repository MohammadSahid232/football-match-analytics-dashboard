"""
test_fifa2026_preprocessing.py
Unit tests for the FIFA 2026 feature engineering and preprocessing.
"""

import unittest
import pandas as pd
import numpy as np
from app.services.fifa2026_preprocessing import (
    engineer_matches, engineer_players, engineer_teams,
    engineer_groups, normalize_dataframe
)


class TestFIFA2026Preprocessing(unittest.TestCase):

    def setUp(self):
        # Mock datasets
        self.mock_matches = pd.DataFrame({
            'MatchID': [1, 2, 3],
            'Round': ['Group Stage', 'Round of 32', 'Final'],
            'HomeTeam': ['United States', 'Mexico', 'Canada'],
            'AwayTeam': ['England', 'Argentina', 'Germany'],
            'HomeGoals': [2, 1, 0],
            'AwayGoals': [1, 1, 3],
            'Winner': ['United States', 'Draw', 'Germany']
        })

        self.mock_players = pd.DataFrame({
            'PlayerID': [1, 2],
            'Name': ['Christian Pulisic', 'Lionel Messi'],
            'Position': ['MF', 'FW'],
            'Goals': [2, 4],
            'Assists': [1, 2],
            'Minutes': [180, 270],
            'Shots': [5, 10],
            'ShotsOnTarget': [3, 6]
        })

        self.mock_teams = pd.DataFrame({
            'TeamID': [1, 2, 3, 4],
            'Nation': ['United States', 'Mexico', 'Canada', 'England'],
            'Confederation': ['CONCACAF', 'CONCACAF', 'CONCACAF', 'UEFA']
        })

        self.mock_groups = pd.DataFrame({
            'Group': ['A', 'A', 'B'],
            'Nation': ['United States', 'England', 'Mexico'],
            'Played': [3, 3, 3],
            'Points': [7, 4, 3],
            'GD': [3, 0, -2]
        })

    def test_engineer_matches(self):
        df_eng = engineer_matches(self.mock_matches)
        # Verify derived columns exist
        self.assertIn('total_goals', df_eng.columns)
        self.assertIn('goal_diff', df_eng.columns)
        self.assertIn('is_draw', df_eng.columns)
        self.assertIn('round_encoded', df_eng.columns)
        self.assertIn('host_played', df_eng.columns)

        # Assert calculations
        self.assertEqual(df_eng.loc[0, 'total_goals'], 3)
        self.assertEqual(df_eng.loc[1, 'goal_diff'], 0)
        self.assertEqual(df_eng.loc[1, 'is_draw'], 1)
        self.assertEqual(df_eng.loc[0, 'round_encoded'], 0)  # Group Stage
        self.assertEqual(df_eng.loc[2, 'round_encoded'], 6)  # Final
        self.assertEqual(df_eng.loc[0, 'host_played'], 1)  # USA (Host)

    def test_engineer_players(self):
        df_eng = engineer_players(self.mock_players)
        self.assertIn('goals_per_90', df_eng.columns)
        self.assertIn('assists_per_90', df_eng.columns)
        self.assertIn('contributions', df_eng.columns)
        self.assertIn('efficiency_score', df_eng.columns)
        self.assertIn('shot_accuracy', df_eng.columns)

        # Pulisic: 2 goals, 180 mins -> 1.0 goal per 90
        self.assertAlmostEqual(df_eng.loc[0, 'goals_per_90'], 1.0)
        self.assertEqual(df_eng.loc[0, 'contributions'], 3)
        # Efficiency: (2*2 + 1) / (180/90) = 5 / 2 = 2.5
        self.assertAlmostEqual(df_eng.loc[0, 'efficiency_score'], 2.5)
        self.assertAlmostEqual(df_eng.loc[0, 'shot_accuracy'], 60.0)

    def test_engineer_teams(self):
        df_eng = engineer_teams(self.mock_matches, self.mock_teams)
        self.assertIn('avg_goals_scored', df_eng.columns)
        self.assertIn('win_rate', df_eng.columns)
        self.assertIn('confederation_encoded', df_eng.columns)

        # United States played 1 match, won it, scored 2 goals, conceded 1
        us_row = df_eng[df_eng['Nation'] == 'United States'].iloc[0]
        self.assertEqual(us_row['Played'], 1)
        self.assertEqual(us_row['Wins'], 1)
        self.assertAlmostEqual(us_row['win_rate'], 1.0)
        self.assertAlmostEqual(us_row['avg_goals_scored'], 2.0)
        self.assertAlmostEqual(us_row['avg_goals_conceded'], 1.0)

    def test_engineer_groups(self):
        df_eng = engineer_groups(self.mock_groups)
        self.assertIn('points_per_game', df_eng.columns)
        self.assertIn('gd_positive', df_eng.columns)
        self.assertAlmostEqual(df_eng.loc[0, 'points_per_game'], 2.33, places=2)
        self.assertEqual(df_eng.loc[0, 'gd_positive'], 1)  # GD = 3
        self.assertEqual(df_eng.loc[2, 'gd_positive'], 0)  # GD = -2

    def test_normalize_dataframe(self):
        df_num = pd.DataFrame({'val1': [10, 20, 30], 'val2': [100, 200, 300]})
        df_scaled = normalize_dataframe(df_num)
        self.assertAlmostEqual(df_scaled['val1'].min(), 0.0)
        self.assertAlmostEqual(df_scaled['val1'].max(), 1.0)
        self.assertAlmostEqual(df_scaled['val2'].min(), 0.0)
        self.assertAlmostEqual(df_scaled['val2'].max(), 1.0)


if __name__ == '__main__':
    unittest.main()
