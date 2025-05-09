"""
اختبارات لواجهة برمجة التطبيقات البسيطة
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# إضافة المجلد الرئيسي إلى مسار البحث
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# استيراد التطبيق البسيط
from test_api import app

client = TestClient(app)

def test_root_endpoint():
    """اختبار نقطة النهاية الرئيسية"""
    response = client.get("/")
    assert response.status_code == 200
    assert "مرحبًا بك في واجهة برمجة تطبيقات Horus للاختبار" in response.json()["message"]

def test_health_endpoint():
    """اختبار نقطة نهاية فحص الصحة"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
