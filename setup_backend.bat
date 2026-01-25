@echo off
echo ========================================
echo Setting up Django Backend
echo ========================================
cd backend

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
echo Creating migrations...
python manage.py makemigrations

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo ========================================
echo Backend setup complete!
echo ========================================
echo.
echo To start the server, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
pause
