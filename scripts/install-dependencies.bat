@echo off
echo === Installing required packages ===

echo Installing FastAPI, Uvicorn, and other dependencies...
pip install fastapi uvicorn python-dotenv pydantic

echo Checking if packages are installed correctly...
pip list | findstr "fastapi"
pip list | findstr "uvicorn"
pip list | findstr "python-dotenv"
pip list | findstr "pydantic"

echo Done.
pause