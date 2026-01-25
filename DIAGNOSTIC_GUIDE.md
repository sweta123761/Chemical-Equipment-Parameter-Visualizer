# Diagnostic Guide: "Still Not Found" Issue

## Understanding "Not Found" Messages

When you see `Not Found: /` in your backend terminal, this is **NORMAL** and **EXPECTED**. It means:
- ✅ Your backend server IS running
- ✅ Someone tried to access the root URL (`http://localhost:8000/`)
- ❌ The root URL doesn't have a view (which is fine - we don't need it)

## What URLs Actually Work

Your API endpoints are at:
- ✅ `http://localhost:8000/api/upload/` - For uploading CSV files
- ✅ `http://localhost:8000/api/history/` - For viewing upload history
- ✅ `http://localhost:8000/api/report/` - For generating PDF reports
- ✅ `http://localhost:8000/admin/` - Django admin panel

The root URL (`http://localhost:8000/`) will show "Not Found" - this is expected!

## Step-by-Step Diagnosis

### Step 1: Verify Backend is Running

**Check your backend terminal.** You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

If you see this, your backend IS running! ✅

### Step 2: Test the API Endpoint

**Option A - Use the test script:**
Double-click `test_backend.bat`

**Option B - Manual test:**
1. Open your browser
2. Go to: `http://localhost:8000/api/history/`
3. You should be prompted for username/password
4. Enter:
   - Username: `admin`
   - Password: `admin123`
5. You should see JSON data (even if it's just `[]`)

**What you should see:**
- ✅ Browser asks for username/password → Backend is running!
- ✅ After entering credentials, you see `[]` or JSON data → Everything works!
- ❌ "This site can't be reached" → Backend is NOT running
- ❌ "401 Unauthorized" → Password is wrong (run `fix_admin_password.bat`)

### Step 3: Check Password

If you get "401 Unauthorized":
1. Stop the backend server (Ctrl+C)
2. Run `fix_admin_password.bat` (or `python create_admin.py` in backend folder)
3. Restart the backend server

### Step 4: Test from Web App

1. Make sure backend is running (Step 1)
2. Make sure web frontend is running (`npm start` in `web-frontend` folder)
3. Go to `http://localhost:3000`
4. Try uploading a CSV file

## Common Issues

### Issue: "This site can't be reached" in browser

**Cause:** Backend server is not running

**Fix:**
1. Open a terminal
2. Navigate to backend folder: `cd backend`
3. Activate virtual environment: `venv\Scripts\activate`
4. Start server: `python manage.py runserver`
5. Wait for: `Starting development server at http://127.0.0.1:8000/`

### Issue: "401 Unauthorized"

**Cause:** Wrong password or user doesn't exist

**Fix:**
1. Stop backend (Ctrl+C)
2. Run `fix_admin_password.bat`
3. Restart backend

### Issue: "Not Found: /" in terminal

**This is NORMAL!** It just means someone accessed the root URL. Ignore these messages.

### Issue: Web app shows "Upload failed"

**Check:**
1. Is backend running? (See Step 1)
2. Is password correct? (See Step 3)
3. Open browser console (F12) and check for errors
4. Check backend terminal for error messages

## Quick Test Checklist

- [ ] Backend terminal shows: `Starting development server at http://127.0.0.1:8000/`
- [ ] Browser can access: `http://localhost:8000/api/history/` (asks for password)
- [ ] After entering `admin` / `admin123`, you see JSON (even if `[]`)
- [ ] Web frontend is running (`npm start`)
- [ ] Web app is open at `http://localhost:3000`

If all checkboxes are checked, everything should work!

## Still Having Issues?

1. **Check backend terminal** - Look for error messages (red text)
2. **Check browser console** - Press F12 → Console tab → Look for errors
3. **Verify password** - Run `fix_admin_password.bat`
4. **Restart everything** - Stop both servers, then start backend first, then web frontend
