@echo off
echo === Checking Dependencies ===

echo Running dependency check...
cd ..
python tests/test_dependencies.py

echo Check completed.
pause
