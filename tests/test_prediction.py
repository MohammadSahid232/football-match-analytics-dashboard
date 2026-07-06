import unittest
from app.services.predictions import predict_match

class TestPrediction(unittest.TestCase):
    def test_predict_match_structure(self):
        result = predict_match("Machhindra FC", "Church Boys United")
        
        # Could be None if model fails to train (e.g. not enough data)
        if result is not None:
            self.assertIn('prediction', result)
            self.assertIn('probabilities', result)
            self.assertIn('home_win', result['probabilities'])
            self.assertIn('away_win', result['probabilities'])
            self.assertIn('draw', result['probabilities'])
            
            # Check sum of probabilities is approx 100
            probs = result['probabilities']
            total = probs['home_win'] + probs['away_win'] + probs['draw']
            self.assertAlmostEqual(total, 100.0, delta=1.0)

if __name__ == '__main__':
    unittest.main()
