@echo off
echo === Running Test API ===

echo Installing required packages...
pip install fastapi uvicorn

echo Running the test API...
cd ..
python tests/test_api.py

echo Test API stopped.
pause
