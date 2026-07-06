import unittest
from app.services.loader import load_teams, load_players, load_matches, load_standings

class TestLoader(unittest.TestCase):
    def test_load_teams(self):
        df = load_teams(processed=False)
        self.assertFalse(df.empty)
        self.assertTrue('TeamID' in df.columns)

    def test_load_players(self):
        df = load_players(processed=False)
        self.assertFalse(df.empty)
        self.assertTrue('PlayerID' in df.columns)

    def test_load_matches(self):
        df = load_matches(processed=False)
        self.assertFalse(df.empty)
        self.assertTrue('MatchID' in df.columns)

    def test_load_standings(self):
        df = load_standings(processed=False)
        self.assertFalse(df.empty)
        self.assertTrue('Points' in df.columns)

if __name__ == '__main__':
    unittest.main()
