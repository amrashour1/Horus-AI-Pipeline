import unittest
from src.core.app_gemini import HorusAIGeminiApp

class TestHorusAIGeminiApp(unittest.TestCase):
    def setUp(self):
        self.app = HorusAIGeminiApp()

    def test_gemini_initialization(self):
        self.assertIsNotNone(self.app.gemini_model)
        self.assertEqual(self.app.mode, 'gemini')

if __name__ == '__main__':
    unittest.main()