import unittest
from src.core.app import HorusAIApp

class TestHorusAIApp(unittest.TestCase):
    def setUp(self):
        self.app = HorusAIApp()

    def test_app_initialization(self):
        self.assertIsNotNone(self.app.model)
        self.assertIsInstance(self.app.config, dict)

if __name__ == '__main__':
    unittest.main()