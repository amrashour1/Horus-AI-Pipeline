"""
اختبارات لملف run.py
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# إضافة المسار الرئيسي للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import run

@patch('argparse.ArgumentParser.parse_args')
@patch('os.system')
def test_run_gemini_mode(mock_system, mock_parse_args):
    """اختبار الوضع gemini"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.gemini = True
    mock_args.vertex = False
    mock_args.api = False
    mock_args.orchestrator = False
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    run.main()
    
    # التحقق من النتائج
    mock_system.assert_called_once_with("python src/core/app_gemini.py")

@patch('argparse.ArgumentParser.parse_args')
@patch('os.system')
def test_run_vertex_mode(mock_system, mock_parse_args):
    """اختبار الوضع vertex"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.gemini = False
    mock_args.vertex = True
    mock_args.api = False
    mock_args.orchestrator = False
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    run.main()
    
    # التحقق من النتائج
    mock_system.assert_called_once_with("python src/core/app.py")

@patch('argparse.ArgumentParser.parse_args')
@patch('os.system')
def test_run_api_mode(mock_system, mock_parse_args):
    """اختبار الوضع api"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.gemini = False
    mock_args.vertex = False
    mock_args.api = True
    mock_args.orchestrator = False
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    run.main()
    
    # التحقق من النتائج
    mock_system.assert_called_once_with("python src/api/api.py")

@patch('argparse.ArgumentParser.parse_args')
@patch('os.system')
def test_run_orchestrator_mode(mock_system, mock_parse_args):
    """اختبار الوضع orchestrator"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.gemini = False
    mock_args.vertex = False
    mock_args.api = False
    mock_args.orchestrator = True
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    run.main()
    
    # التحقق من النتائج
    mock_system.assert_called_once_with("python src/core/orchestrator.py")

@patch('argparse.ArgumentParser.parse_args')
@patch('os.system')
def test_run_default_mode(mock_system, mock_parse_args):
    """اختبار الوضع الافتراضي"""
    # تعيين قيم وهمية
    mock_args = MagicMock()
    mock_args.gemini = False
    mock_args.vertex = False
    mock_args.api = False
    mock_args.orchestrator = False
    mock_parse_args.return_value = mock_args
    
    # تنفيذ الاختبار
    run.main()
    
    # التحقق من النتائج
    mock_system.assert_called_once_with("python src/core/app_gemini.py")
