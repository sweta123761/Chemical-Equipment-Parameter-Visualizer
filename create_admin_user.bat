@echo off
echo ========================================
echo Creating Admin User
echo ========================================
cd backend

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Creating admin user (username: admin, password: admin123)...
python create_admin.py

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo You can now use:
echo   Username: admin
echo   Password: admin123
echo.
pause
