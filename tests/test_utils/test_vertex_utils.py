"""
اختبارات لوحدة vertex_utils
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import vertex_utils

@patch('google.cloud.aiplatform.init')
@patch('vertexai.init')
def test_init_vertex(mock_vertexai_init, mock_aiplatform_init):
    """اختبار تهيئة Vertex AI"""
    # تنفيذ الاختبار بدون ملف اعتماد
    vertex_utils.init_vertex("test-project", "test-location")
    
    # التحقق من النتائج
    mock_aiplatform_init.assert_called_once_with(
        project="test-project",
        location="test-location"
    )
    mock_vertexai_init.assert_called_once_with(
        project="test-project",
        location="test-location"
    )

@patch('google.oauth2.service_account.Credentials.from_service_account_file')
@patch('google.cloud.aiplatform.init')
@patch('vertexai.init')
def test_init_vertex_with_credentials(mock_vertexai_init, mock_aiplatform_init, mock_credentials):
    """اختبار تهيئة Vertex AI مع اعتمادات"""
    # تعيين قيم وهمية
    mock_creds = MagicMock()
    mock_credentials.return_value = mock_creds
    
    # تنفيذ الاختبار مع ملف اعتماد
    with patch('os.path.exists', return_value=True):
        vertex_utils.init_vertex("test-project", "test-location", "fake-credentials.json")
    
    # التحقق من النتائج
    mock_credentials.assert_called_once_with("fake-credentials.json")
    mock_aiplatform_init.assert_called_once_with(
        project="test-project",
        location="test-location",
        credentials=mock_creds
    )
    mock_vertexai_init.assert_called_once_with(
        project="test-project",
        location="test-location",
        credentials=mock_creds
    )

@patch('vertexai.generative_models.GenerativeModel')
def test_get_gemini_model(mock_generative_model):
    """اختبار الحصول على نموذج Gemini"""
    # تعيين قيم وهمية
    mock_model = MagicMock()
    mock_generative_model.return_value = mock_model
    
    # تنفيذ الاختبار
    model = vertex_utils.get_gemini_model("test-model")
    
    # التحقق من النتائج
    assert model == mock_model
    mock_generative_model.assert_called_once_with("test-model")

def test_call_gemini_direct(mock_vertex_model):
    """اختبار استدعاء نموذج Gemini مباشرة"""
    # تنفيذ الاختبار
    prompt = "اختبار"
    response = vertex_utils.call_gemini_direct(mock_vertex_model, prompt)
    
    # التحقق من النتائج
    assert "استجابة وهمية" in response

@patch('vertexai.generative_models.GenerativeModel.generate_content')
def test_call_gemini_direct_exception(mock_generate_content):
    """اختبار استدعاء نموذج Gemini مع استثناء"""
    # تعيين قيم وهمية
    mock_generate_content.side_effect = Exception("خطأ اختبار")
    
    mock_model = MagicMock()
    mock_model.generate_content = mock_generate_content
    
    # تنفيذ الاختبار
    with pytest.raises(Exception):
        vertex_utils.call_gemini_direct(mock_model, "اختبار")
