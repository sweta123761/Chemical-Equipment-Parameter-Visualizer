@echo off
echo ========================================
echo Testing Backend API
echo ========================================
echo.
echo This script will test if your backend is working correctly.
echo.
echo Make sure your backend server is running first!
echo (You should see "Starting development server at http://127.0.0.1:8000/")
echo.
pause

echo.
echo Testing API endpoint: http://localhost:8000/api/history/
echo.
echo Opening in browser... (you'll need to enter username: admin, password: admin123)
start http://localhost:8000/api/history/

echo.
echo ========================================
echo Test Instructions:
echo ========================================
echo.
echo 1. A browser window should open asking for username/password
echo 2. Enter:
echo    Username: admin
echo    Password: admin123
echo 3. You should see JSON data (even if it's just [])
echo.
echo If you see "401 Unauthorized":
echo   - Run fix_admin_password.bat to reset the password
echo.
echo If you see "This site can't be reached":
echo   - Your backend server is not running
echo   - Start it with: start_backend.bat
echo.
echo If you see JSON data (even []):
echo   - Your backend is working correctly! ✓
echo.
pause
