# Fix: "no such table: equipment_equipmentupload"

This error means the database tables haven't been created yet. Here's how to fix it:

## Quick Fix

**Option 1 - Use the script (Easiest):**
1. **Stop your backend server** (Press Ctrl+C in the backend terminal)
2. Double-click `fix_database.bat` in the project root
3. Restart your backend server

**Option 2 - Manual fix:**
1. **Stop your backend server** (Press Ctrl+C)
2. Open a terminal in the `backend` folder
3. Activate virtual environment: `venv\Scripts\activate`
4. Create migrations: `python manage.py makemigrations`
5. Run migrations: `python manage.py migrate`
6. Restart your backend server: `python manage.py runserver`

## What This Does

- **makemigrations**: Creates migration files based on your models
- **migrate**: Creates the actual database tables in SQLite

## After Running

Once you've run the migrations:
1. Restart your backend server
2. Try uploading a CSV file again
3. It should work now!

## Why This Happened

Django needs to create database tables based on your models. The `EquipmentUpload` model exists in code, but the database table wasn't created yet. Running migrations creates the table.
