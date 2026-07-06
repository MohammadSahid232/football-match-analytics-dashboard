import unittest
import pandas as pd
from app.services.preprocessing import clean_teams, clean_players

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.raw_teams = pd.DataFrame([
            {'TeamID': 1, 'Name': 'Team A ', 'Founded': '1990', 'Capacity': '5000'},
            {'TeamID': 1, 'Name': 'Team A ', 'Founded': '1990', 'Capacity': '5000'}
        ])
        
        self.raw_players = pd.DataFrame([
            {'PlayerID': 1, 'Name': 'Player A', 'Goals': '', 'Rating': 'NaN', 'Assists': '', 'Yellow Cards': '', 'Red Cards': '', 'Matches Played': '', 'Minutes Played': '', 'Age': '', 'Position': 'forward'},
            {'PlayerID': 2, 'Name': 'Player B', 'Goals': '2', 'Rating': '7.5', 'Assists': '1', 'Yellow Cards': '0', 'Red Cards': '0', 'Matches Played': '1', 'Minutes Played': '90', 'Age': '25', 'Position': 'midfielder'}
        ])

    def test_clean_teams(self):
        cleaned = clean_teams(self.raw_teams)
        # Should drop duplicate
        self.assertEqual(len(cleaned), 1)
        # Should strip whitespace
        self.assertEqual(cleaned.iloc[0]['Name'], 'Team A')
        # Should convert types
        self.assertTrue(pd.api.types.is_integer_dtype(cleaned['Founded']))

    def test_clean_players(self):
        cleaned = clean_players(self.raw_players)
        # Fill missing numeric values with 0
        self.assertEqual(cleaned.iloc[0]['Goals'], 0)
        # Fill missing rating with 6.0
        self.assertEqual(cleaned.iloc[0]['Rating'], 6.0)

if __name__ == '__main__':
    unittest.main()
