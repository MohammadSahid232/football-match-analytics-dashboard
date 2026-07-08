"""
test_fifa2026_cleaning.py
Unit tests for the FIFA 2026 data cleaning pipeline.
"""

import unittest
import pandas as pd
import numpy as np
from app.services.fifa2026_cleaning import (
    drop_duplicates, strip_strings, fill_missing_numeric,
    fill_missing_categorical, convert_dates, validate_goals,
    remove_outliers_iqr
)


class TestFIFA2026Cleaning(unittest.TestCase):

    def setUp(self):
        # Create a mock DataFrame with dirty data
        self.mock_df = pd.DataFrame({
            'MatchID': [1, 2, 2, 3, 4],  # Row 2 is a duplicate
            'HomeTeam': [' USA ', 'Mexico', 'Mexico', 'Canada', ' Argentina'],
            'AwayTeam': ['England', 'Brazil', 'Brazil', None, 'France'],
            'HomeGoals': [2, 1, 1, -1, 3],  # HomeGoals has negative value
            'AwayGoals': [1, np.nan, np.nan, 2, 0],  # AwayGoals has NaN
            'Date': ['2026-06-11', '2026-06-12', '2026-06-12', '2026-06-13', '2026-06-14'],
            'Attendance': [70000, 80000, 80000, 65000, 150000]  # 150000 is an outlier
        })

    def test_drop_duplicates(self):
        df_cleaned = drop_duplicates(self.mock_df)
        self.assertEqual(len(df_cleaned), 4)
        self.assertEqual(df_cleaned['MatchID'].tolist(), [1, 2, 3, 4])

    def test_strip_strings(self):
        df_cleaned = strip_strings(self.mock_df)
        self.assertEqual(df_cleaned.loc[0, 'HomeTeam'], 'USA')
        self.assertEqual(df_cleaned.loc[4, 'HomeTeam'], 'Argentina')

    def test_fill_missing_numeric(self):
        df_cleaned = fill_missing_numeric(self.mock_df)
        # Median of [1.0, 1.0, 2.0, 0.0] is 1.0
        self.assertEqual(df_cleaned.loc[1, 'AwayGoals'], 1.0)
        self.assertFalse(df_cleaned['AwayGoals'].isna().any())

    def test_fill_missing_categorical(self):
        # Mode of ['England', 'Brazil', 'Brazil', 'France'] is 'Brazil'
        df_cleaned = fill_missing_categorical(self.mock_df)
        self.assertEqual(df_cleaned.loc[3, 'AwayTeam'], 'Brazil')
        self.assertFalse(df_cleaned['AwayTeam'].isna().any())

    def test_convert_dates(self):
        df_cleaned = convert_dates(self.mock_df, 'Date')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_cleaned['Date']))

    def test_validate_goals(self):
        df_cleaned = validate_goals(self.mock_df)
        # Negative HomeGoals clipped to 0
        self.assertEqual(df_cleaned.loc[3, 'HomeGoals'], 0)
        self.assertTrue((df_cleaned['HomeGoals'] >= 0).all())

    def test_remove_outliers_iqr(self):
        # Remove outlier on Attendance
        df_cleaned = remove_outliers_iqr(self.mock_df, 'Attendance')
        # Row with 150000 should be removed
        self.assertNotIn(150000, df_cleaned['Attendance'].tolist())
        self.assertTrue(len(df_cleaned) < len(self.mock_df))


if __name__ == '__main__':
    unittest.main()
