import unittest
from src.core.main_pipeline import MainPipeline

class TestMainPipeline(unittest.TestCase):
    def test_pipeline_flow(self):
        pipeline = MainPipeline()
        self.assertTrue(pipeline.validate_steps())

if __name__ == '__main__':
    unittest.main()