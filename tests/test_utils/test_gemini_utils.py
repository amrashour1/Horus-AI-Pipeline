"""
اختبارات لوحدة gemini_utils
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import gemini_utils

@patch('google.generativeai.configure')
def test_init_gemini_api(mock_configure):
    """اختبار تهيئة Gemini API"""
    # تعيين قيمة وهمية لمتغير البيئة
    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_api_key"}):
        result = gemini_utils.init_gemini_api()
        assert result is True
        mock_configure.assert_called_once_with(api_key="fake_api_key")

@patch('google.generativeai.configure')
def test_init_gemini_api_missing_key(mock_configure):
    """اختبار تهيئة Gemini API مع مفتاح مفقود"""
    # تعيين قيمة فارغة لمتغير البيئة
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        result = gemini_utils.init_gemini_api()
        assert result is False
        mock_configure.assert_not_called()

@patch('google.generativeai.GenerativeModel')
def test_get_gemini_model(mock_generative_model):
    """اختبار الحصول على نموذج Gemini"""
    mock_model = MagicMock()
    mock_generative_model.return_value = mock_model
    
    model = gemini_utils.get_gemini_model("test-model")
    assert model == mock_model
    mock_generative_model.assert_called_once_with("test-model")

def test_call_gemini_direct(mock_gemini_model):
    """اختبار استدعاء نموذج Gemini مباشرة"""
    prompt = "اختبار"
    response = gemini_utils.call_gemini_direct(mock_gemini_model, prompt)
    assert "استجابة وهمية" in response

@patch('google.generativeai.GenerativeModel.generate_content')
def test_call_gemini_direct_exception(mock_generate_content):
    """اختبار استدعاء نموذج Gemini مع استثناء"""
    mock_generate_content.side_effect = Exception("خطأ اختبار")
    
    mock_model = MagicMock()
    mock_model.generate_content = mock_generate_content
    
    with pytest.raises(Exception):
        gemini_utils.call_gemini_direct(mock_model, "اختبار")
