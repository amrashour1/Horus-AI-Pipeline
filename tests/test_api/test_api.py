"""
اختبارات لوحدة api
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# استيراد التطبيق بعد تعيين المسار
with patch('src.utils.gemini_utils.init_gemini_api', return_value=True), \
     patch('src.utils.gemini_utils.get_gemini_model', return_value=MagicMock()):
    from src.api.api import app

client = TestClient(app)

def test_read_root():
    """اختبار نقطة النهاية الرئيسية"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Horus AI Pipeline API" in response.json()["message"]

def test_health_check():
    """اختبار فحص الصحة"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@patch('src.core.app_gemini.process_query')
def test_analyze_text(mock_process_query):
    """اختبار تحليل النص"""
    mock_process_query.return_value = "تحليل وهمي"
    
    response = client.post(
        "/analyze",
        json={"text": "نص اختبار"}
    )
    
    assert response.status_code == 200
    assert response.json()["analysis"] == "تحليل وهمي"
    mock_process_query.assert_called_once()

def test_analyze_text_empty():
    """اختبار تحليل النص الفارغ"""
    response = client.post(
        "/analyze",
        json={"text": ""}
    )
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_get_models():
    """اختبار الحصول على النماذج المتاحة"""
    response = client.get("/models")
    assert response.status_code == 200
    assert isinstance(response.json()["models"], list)
    assert len(response.json()["models"]) > 0
