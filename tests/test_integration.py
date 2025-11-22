import unittest
from src.backend.dashboard import generate_dashboard_data

class TestIntegration(unittest.TestCase):
    def test_dashboard_generation(self):
        data = generate_dashboard_data()
        self.assertIn('profile', data)
        self.assertIn('weather', data)
        self.assertIn('soil', data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
