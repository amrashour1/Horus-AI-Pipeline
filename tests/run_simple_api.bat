@echo off
echo === Running Simple API ===

echo Installing required packages...
pip install fastapi uvicorn

echo Running the simple API...
cd ..
python tests/simple_api.py

echo Simple API stopped.
pause
