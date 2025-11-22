import unittest
from src.backend.crop_recommender import calculate_npk_match

class TestCropRecommender(unittest.TestCase):
    def test_npk_match_calculation(self):
        soil = {'N': 200, 'P': 50, 'K': 50}
        crop = {'N': 200, 'P': 50, 'K': 50}
        score = calculate_npk_match(soil, crop)
        self.assertEqual(score, 100.0)
    
    def test_npk_mismatch(self):
        soil = {'N': 100, 'P': 25, 'K': 25}
        crop = {'N': 200, 'P': 50, 'K': 50}
        score = calculate_npk_match(soil, crop)
        self.assertLess(score, 100.0)

if __name__ == '__main__':
    unittest.main()
