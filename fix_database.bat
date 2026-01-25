@echo off
echo ========================================
echo Fixing Database - Creating Tables
echo ========================================
cd backend

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Creating migrations...
python manage.py makemigrations

echo.
echo Running migrations to create database tables...
python manage.py migrate

echo.
echo ========================================
echo Database setup complete!
echo ========================================
echo.
echo The database tables have been created.
echo You can now restart your backend server.
echo.
pause
