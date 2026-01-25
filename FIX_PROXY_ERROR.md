# Fix: "Proxy error: Could not proxy request... ECONNREFUSED"

This error means your **backend server is not running**. The React app is trying to connect to the backend on port 8000, but it can't find it.

## Quick Fix

### Step 1: Start the Backend Server

**Option A - Use the script:**
Double-click `start_backend.bat` in the project root folder.

**Option B - Manual:**
1. Open a NEW terminal/command prompt
2. Navigate to backend folder:
   ```bash
   cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro\backend"
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

### Step 2: Verify Backend is Running

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Keep this terminal window open!** The backend must stay running.

### Step 3: Check Your Web App

The proxy errors should stop once the backend is running. Try uploading a CSV file again.

## What's Happening

- **Web Frontend (React)**: Running on port 3000 ✅
- **Backend (Django)**: Should be running on port 8000 ❌ (Not running)
- **Proxy**: React tries to forward API requests to backend, but can't connect

## Important: Running Order

Always start in this order:
1. **First**: Start Backend (`start_backend.bat` or `python manage.py runserver`)
2. **Second**: Start Web Frontend (`npm start` in `web-frontend` folder)

## If Backend Won't Start

If you get errors when starting the backend:
1. Make sure you're in the `backend` folder
2. Make sure virtual environment is activated
3. Make sure dependencies are installed: `pip install -r requirements.txt`
4. Make sure database is set up: Run `fix_database.bat` first
