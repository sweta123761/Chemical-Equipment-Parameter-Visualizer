@echo off
echo Starting Desktop Application...
echo Make sure the backend server is running first!
cd desktop-app
call venv\Scripts\activate.bat
python main.py
pause
