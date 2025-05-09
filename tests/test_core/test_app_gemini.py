"""
اختبارات لوحدة app_gemini
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core import app_gemini

@patch('src.utils.gemini_utils.init_gemini_api')
def test_initialize_gemini_api(mock_init_gemini_api):
    """اختبار تهيئة Gemini API"""
    mock_init_gemini_api.return_value = True
    result = app_gemini.initialize_gemini_api()
    assert result is True
    mock_init_gemini_api.assert_called_once()

@patch('src.utils.gemini_utils.get_gemini_model')
def test_get_model(mock_get_gemini_model):
    """اختبار الحصول على نموذج Gemini"""
    mock_model = MagicMock()
    mock_get_gemini_model.return_value = mock_model
    
    model = app_gemini.get_model()
    assert model == mock_model
    mock_get_gemini_model.assert_called_once()

@patch('src.utils.memory_utils.context_reminder')
@patch('src.utils.gemini_utils.call_gemini_direct')
def test_process_query(mock_call_gemini_direct, mock_context_reminder, mock_gemini_model):
    """اختبار معالجة استعلام المستخدم"""
    # تعيين قيم وهمية
    mock_context_reminder.return_value = "سياق وهمي"
    mock_call_gemini_direct.return_value = "استجابة وهمية"
    
    # حفظ القيم الأصلية
    original_chat_history = app_gemini.chat_history.copy()
    
    # تنفيذ الاختبار
    query = "استعلام اختبار"
    response = app_gemini.process_query(query, mock_gemini_model)
    
    # التحقق من النتائج
    assert response == "استجابة وهمية"
    mock_context_reminder.assert_called_once()
    mock_call_gemini_direct.assert_called_once()
    
    # التحقق من تحديث تاريخ المحادثة
    assert len(app_gemini.chat_history) == len(original_chat_history) + 2
    assert app_gemini.chat_history[-2]["role"] == "user"
    assert app_gemini.chat_history[-2]["content"] == "استعلام اختبار"
    assert app_gemini.chat_history[-1]["role"] == "assistant"
    assert app_gemini.chat_history[-1]["content"] == "استجابة وهمية"
    
    # إعادة تعيين تاريخ المحادثة
    app_gemini.chat_history = original_chat_history

@patch('src.utils.memory_utils.context_reminder')
@patch('src.utils.gemini_utils.call_gemini_direct')
def test_process_query_exception(mock_call_gemini_direct, mock_context_reminder, mock_gemini_model):
    """اختبار معالجة استعلام المستخدم مع استثناء"""
    # تعيين قيم وهمية
    mock_context_reminder.return_value = "سياق وهمي"
    mock_call_gemini_direct.side_effect = Exception("خطأ اختبار")
    
    # حفظ القيم الأصلية
    original_chat_history = app_gemini.chat_history.copy()
    
    # تنفيذ الاختبار
    query = "استعلام اختبار"
    response = app_gemini.process_query(query, mock_gemini_model)
    
    # التحقق من النتائج
    assert "عذراً، حدث خطأ" in response
    assert "خطأ اختبار" in response
    mock_context_reminder.assert_called_once()
    mock_call_gemini_direct.assert_called_once()
    
    # التحقق من عدم تحديث تاريخ المحادثة
    assert app_gemini.chat_history == original_chat_history
