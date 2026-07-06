import unittest
from app.services.statistics import get_league_summary, get_top_scorers

class TestStatistics(unittest.TestCase):
    def test_league_summary(self):
        summary = get_league_summary()
        self.assertIn('total_matches', summary)
        self.assertIn('total_goals', summary)
        self.assertIn('avg_goals', summary)
        self.assertTrue(isinstance(summary['total_matches'], int))
        
    def test_top_scorers(self):
        top = get_top_scorers(limit=5)
        self.assertIsInstance(top, list)
        if len(top) > 0:
            self.assertIn('Goals', top[0])
            self.assertIn('Name', top[0])

if __name__ == '__main__':
    unittest.main()
