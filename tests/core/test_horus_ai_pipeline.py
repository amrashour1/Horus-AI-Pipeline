import unittest
from src.core.horus_ai_pipeline import HorusAIPipeline

class TestHorusAIPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = HorusAIPipeline()

    def test_pipeline_execution(self):
        self.assertTrue(self.pipeline.validate_configuration())

if __name__ == '__main__':
    unittest.main()