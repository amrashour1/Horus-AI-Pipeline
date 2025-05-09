"""
ملف التكوين لاختبارات pytest
"""

import os
import sys
import pytest

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_gemini_model():
    """
    fixture لنموذج Gemini وهمي
    """
    class MockGeminiModel:
        def generate_content(self, prompt, generation_config=None):
            class MockResponse:
                @property
                def text(self):
                    return f"استجابة وهمية لـ: {prompt}"
            return MockResponse()
    
    return MockGeminiModel()

@pytest.fixture
def mock_vertex_model():
    """
    fixture لنموذج Vertex AI وهمي
    """
    class MockVertexModel:
        def predict_text(self, prompt):
            return f"استجابة وهمية لـ: {prompt}"
    
    return MockVertexModel()

@pytest.fixture
def mock_memory():
    """
    fixture لذاكرة وهمية
    """
    class MockMemory:
        def __init__(self):
            self.data = {}
        
        def add(self, items):
            if isinstance(items, list):
                for i, item in enumerate(items):
                    self.data[f"item_{i}"] = item
            else:
                self.data["item"] = items
        
        def get(self, key, default=None):
            return self.data.get(key, default)
        
        def query(self, query_texts, n_results=1):
            return {
                "documents": ["وثيقة وهمية 1", "وثيقة وهمية 2"],
                "metadatas": [{"source": "وهمي"}, {"source": "وهمي"}],
                "distances": [0.1, 0.2]
            }
    
    return MockMemory()
