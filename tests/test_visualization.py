import unittest
from app.services.visualization import generate_top_scorers_chart, generate_team_points_chart, generate_goals_distribution_chart, generate_all_charts

class TestVisualization(unittest.TestCase):
    def test_chart_generation_returns_paths(self):
        # We don't want to actually generate the image for tests, just check the string logic
        # But since the function executes Matplotlib, we'll verify it doesn't crash
        # and returns a string path ending in .png
        path1 = generate_top_scorers_chart()
        path2 = generate_team_points_chart()
        path3 = generate_goals_distribution_chart()
        
        self.assertTrue(path1.endswith('.png'))
        self.assertTrue(path2.endswith('.png'))
        self.assertTrue(path3.endswith('.png'))
        
    def test_generate_all_charts(self):
        charts = generate_all_charts()
        self.assertIn('top_scorers', charts)
        self.assertIn('team_points', charts)
        self.assertIn('goals_distribution', charts)

if __name__ == '__main__':
    unittest.main()
