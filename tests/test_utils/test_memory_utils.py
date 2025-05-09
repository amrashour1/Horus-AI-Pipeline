"""
اختبارات لوحدة memory_utils
"""

import pytest
import os
import sys

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import memory_utils

def test_init_working_memory():
    """اختبار تهيئة الذاكرة العاملة"""
    memory = memory_utils.init_working_memory()
    assert memory is not None

def test_init_long_term_memory():
    """اختبار تهيئة الذاكرة طويلة المدى"""
    memory = memory_utils.init_long_term_memory()
    assert memory is not None

def test_context_reminder_with_empty_history():
    """اختبار استرجاع السياق مع تاريخ فارغ"""
    query = "استعلام اختبار"
    chat_hist = []
    
    # استخدام ذاكرة وهمية
    mock_memory = type('obj', (object,), {
        'query': lambda query_texts, n_results: {
            'documents': ['وثيقة اختبار']
        }
    })
    
    result = memory_utils.context_reminder(query, chat_hist, mock_memory)
    assert "وثيقة اختبار" in result
    assert "سياق حديث: []" in result

def test_context_reminder_with_history():
    """اختبار استرجاع السياق مع تاريخ"""
    query = "استعلام اختبار"
    chat_hist = [
        {"role": "user", "content": "سؤال 1"},
        {"role": "assistant", "content": "إجابة 1"},
        {"role": "user", "content": "سؤال 2"},
        {"role": "assistant", "content": "إجابة 2"}
    ]
    
    # استخدام ذاكرة وهمية
    mock_memory = type('obj', (object,), {
        'query': lambda query_texts, n_results: {
            'documents': ['وثيقة اختبار']
        }
    })
    
    result = memory_utils.context_reminder(query, chat_hist, mock_memory)
    assert "وثيقة اختبار" in result
    assert "سياق حديث:" in result
    assert len(result) > 0

def test_context_reminder_without_memory():
    """اختبار استرجاع السياق بدون ذاكرة"""
    query = "استعلام اختبار"
    chat_hist = []
    
    result = memory_utils.context_reminder(query, chat_hist)
    assert "لا توجد محادثات سابقة" in result
