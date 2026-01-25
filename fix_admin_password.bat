@echo off
echo ========================================
echo Fixing Admin Password
echo ========================================
cd backend

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Resetting admin password to 'admin123'...
python create_admin.py

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo The admin user password has been reset to 'admin123'
echo You can now use:
echo   Username: admin
echo   Password: admin123
echo.
echo Make sure your backend server is running!
echo.
pause
