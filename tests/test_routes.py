import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_teams_route(self):
        response = self.client.get('/teams')
        self.assertEqual(response.status_code, 200)

    def test_players_route(self):
        response = self.client.get('/players')
        self.assertEqual(response.status_code, 200)

    def test_matches_route(self):
        response = self.client.get('/matches')
        self.assertEqual(response.status_code, 200)

    def test_statistics_route(self):
        response = self.client.get('/statistics')
        self.assertEqual(response.status_code, 200)

    def test_analytics_route(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)

    def test_prediction_route_get(self):
        response = self.client.get('/prediction')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
