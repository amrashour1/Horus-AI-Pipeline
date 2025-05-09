"""
اختبارات لوحدة orchestrator
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core import orchestrator

@patch('src.utils.vertex_utils.init_vertex')
def test_initialize_vertex_ai(mock_init_vertex):
    """اختبار تهيئة Vertex AI"""
    # تعيين قيم وهمية
    mock_init_vertex.return_value = None
    
    # تنفيذ الاختبار
    result = orchestrator.initialize_vertex_ai()
    
    # التحقق من النتائج
    assert result is True
    mock_init_vertex.assert_called_once()

@patch('src.utils.vertex_utils.get_gemini_model')
def test_get_model(mock_get_gemini_model):
    """اختبار الحصول على نموذج Gemini"""
    # تعيين قيم وهمية
    mock_model = MagicMock()
    mock_get_gemini_model.return_value = mock_model
    
    # تنفيذ الاختبار
    model = orchestrator.get_model("test-model")
    
    # التحقق من النتائج
    assert model == mock_model
    mock_get_gemini_model.assert_called_once_with("test-model")

@patch('src.utils.vertex_utils.call_gemini_direct')
def test_process_text(mock_call_gemini_direct, mock_vertex_model):
    """اختبار معالجة النص"""
    # تعيين قيم وهمية
    mock_call_gemini_direct.return_value = "تحليل وهمي"
    
    # تنفيذ الاختبار
    text = "نص اختبار"
    result = orchestrator.process_text(text, mock_vertex_model)
    
    # التحقق من النتائج
    assert result == "تحليل وهمي"
    mock_call_gemini_direct.assert_called_once()

@patch('src.utils.vertex_utils.call_gemini_direct')
def test_process_text_exception(mock_call_gemini_direct, mock_vertex_model):
    """اختبار معالجة النص مع استثناء"""
    # تعيين قيم وهمية
    mock_call_gemini_direct.side_effect = Exception("خطأ اختبار")
    
    # تنفيذ الاختبار
    text = "نص اختبار"
    result = orchestrator.process_text(text, mock_vertex_model)
    
    # التحقق من النتائج
    assert "خطأ في معالجة النص" in result
    assert "خطأ اختبار" in result
    mock_call_gemini_direct.assert_called_once()

@patch('concurrent.futures.ThreadPoolExecutor')
def test_process_batch(mock_executor, mock_vertex_model):
    """اختبار معالجة دفعة من النصوص"""
    # تعيين قيم وهمية
    mock_future = MagicMock()
    mock_future.result.return_value = "تحليل وهمي"
    
    mock_executor_instance = MagicMock()
    mock_executor_instance.submit.return_value = mock_future
    mock_executor.return_value.__enter__.return_value = mock_executor_instance
    
    # تنفيذ الاختبار
    texts = ["نص 1", "نص 2", "نص 3"]
    results = orchestrator.process_batch(texts, mock_vertex_model)
    
    # التحقق من النتائج
    assert len(results) == 3
    assert all(result == "تحليل وهمي" for result in results)
    assert mock_executor_instance.submit.call_count == 3
