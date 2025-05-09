"""
اختبارات لملف main.py
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

@patch('argparse.ArgumentParser.parse_args')
@patch('src.core.app.main')
def test_main_vertex_mode(mock_app_main, mock_parse_args):
    """اختبار الوضع vertex"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.mode = "vertex"
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    main.main()
    
    # التحقق من النتائج
    mock_app_main.assert_called_once()

@patch('argparse.ArgumentParser.parse_args')
@patch('src.core.app_gemini.main')
def test_main_gemini_mode(mock_gemini_main, mock_parse_args):
    """اختبار الوضع gemini"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.mode = "gemini"
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    main.main()
    
    # التحقق من النتائج
    mock_gemini_main.assert_called_once()

@patch('argparse.ArgumentParser.parse_args')
@patch('uvicorn.run')
def test_main_api_mode(mock_uvicorn_run, mock_parse_args):
    """اختبار الوضع api"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.mode = "api"
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    with patch('src.api.api.app', 'mock_app'):
        main.main()
    
    # التحقق من النتائج
    mock_uvicorn_run.assert_called_once()

@patch('argparse.ArgumentParser.parse_args')
@patch('src.core.orchestrator.main')
def test_main_orchestrator_mode(mock_orchestrator_main, mock_parse_args):
    """اختبار الوضع orchestrator"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.mode = "orchestrator"
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    main.main()
    
    # التحقق من النتائج
    mock_orchestrator_main.assert_called_once()
