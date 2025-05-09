"""
اختبارات لوحدة app
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core import app

@patch('src.utils.vertex_utils.init_vertex')
def test_initialize_vertex_ai(mock_init_vertex):
    """اختبار تهيئة Vertex AI"""
    # تعيين قيم وهمية
    mock_init_vertex.return_value = None
    
    # تنفيذ الاختبار
    result = app.initialize_vertex_ai()
    
    # التحقق من النتائج
    assert result is True
    mock_init_vertex.assert_called_once()

@patch('src.utils.vertex_utils.init_vertex')
def test_initialize_vertex_ai_exception(mock_init_vertex):
    """اختبار تهيئة Vertex AI مع استثناء"""
    # تعيين قيم وهمية
    mock_init_vertex.side_effect = Exception("خطأ اختبار")
    
    # تنفيذ الاختبار
    result = app.initialize_vertex_ai()
    
    # التحقق من النتائج
    assert result is False
    mock_init_vertex.assert_called_once()

@patch('src.utils.vertex_utils.get_gemini_model')
def test_get_model(mock_get_gemini_model):
    """اختبار الحصول على نموذج Gemini"""
    # تعيين قيم وهمية
    mock_model = MagicMock()
    mock_get_gemini_model.return_value = mock_model
    
    # تنفيذ الاختبار
    model = app.get_model()
    
    # التحقق من النتائج
    assert model == mock_model
    mock_get_gemini_model.assert_called_once()

@patch('src.utils.memory_utils.context_reminder')
@patch('src.utils.vertex_utils.call_gemini_direct')
def test_process_query(mock_call_gemini_direct, mock_context_reminder, mock_vertex_model):
    """اختبار معالجة استعلام المستخدم"""
    # تعيين قيم وهمية
    mock_context_reminder.return_value = "سياق وهمي"
    mock_call_gemini_direct.return_value = "استجابة وهمية"
    
    # حفظ القيم الأصلية
    original_chat_history = app.chat_history.copy()
    
    # تنفيذ الاختبار
    query = "استعلام اختبار"
    response = app.process_query(query, mock_vertex_model)
    
    # التحقق من النتائج
    assert response == "استجابة وهمية"
    mock_context_reminder.assert_called_once()
    mock_call_gemini_direct.assert_called_once()
    
    # التحقق من تحديث تاريخ المحادثة
    assert len(app.chat_history) == len(original_chat_history) + 2
    assert app.chat_history[-2]["role"] == "user"
    assert app.chat_history[-2]["content"] == "استعلام اختبار"
    assert app.chat_history[-1]["role"] == "assistant"
    assert app.chat_history[-1]["content"] == "استجابة وهمية"
    
    # إعادة تعيين تاريخ المحادثة
    app.chat_history = original_chat_history

@patch('src.utils.memory_utils.context_reminder')
@patch('src.utils.vertex_utils.call_gemini_direct')
def test_process_query_exception(mock_call_gemini_direct, mock_context_reminder, mock_vertex_model):
    """اختبار معالجة استعلام المستخدم مع استثناء"""
    # تعيين قيم وهمية
    mock_context_reminder.return_value = "سياق وهمي"
    mock_call_gemini_direct.side_effect = Exception("خطأ اختبار")
    
    # حفظ القيم الأصلية
    original_chat_history = app.chat_history.copy()
    
    # تنفيذ الاختبار
    query = "استعلام اختبار"
    response = app.process_query(query, mock_vertex_model)
    
    # التحقق من النتائج
    assert "عذراً، حدث خطأ" in response
    assert "خطأ اختبار" in response
    mock_context_reminder.assert_called_once()
    mock_call_gemini_direct.assert_called_once()
    
    # التحقق من عدم تحديث تاريخ المحادثة
    assert app.chat_history == original_chat_history
