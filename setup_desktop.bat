@echo off
echo ========================================
echo Setting up PyQt5 Desktop App
echo ========================================
cd desktop-app

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Desktop app setup complete!
echo ========================================
echo.
echo To run the desktop app, run:
echo   cd desktop-app
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Make sure the backend server is running first!
echo.
pause
