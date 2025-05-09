@echo off
echo === Running API Tests ===

echo Installing required packages...
pip install pytest pytest-cov fastapi uvicorn httpx

echo Running tests...
cd ..
python -m pytest tests/test_api/test_simple_api.py -v

echo Tests completed.
pause
