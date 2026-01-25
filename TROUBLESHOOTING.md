# Troubleshooting: "Upload failed. Please try again."

This error means the web frontend cannot connect to the Django backend server. Here's how to fix it:

## Quick Diagnosis Checklist

### ✅ Step 1: Is the Backend Server Running?

**Check:** Open a browser and go to: `http://localhost:8000`

**Expected Result:**
- You should see a Django page (even if it says "Page not found" or shows Django REST Framework)
- If you see "This site can't be reached" or "Connection refused", the backend is NOT running

**If backend is NOT running:**

1. Open a new terminal/command prompt
2. Navigate to the backend folder:
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
5. You should see:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```
6. **Keep this terminal window open!**

---

### ✅ Step 2: Are Backend Dependencies Installed?

**Check:** In the backend terminal, try:
```bash
python manage.py runserver
```

**If you see errors like:**
- `ModuleNotFoundError: No module named 'django'`
- `ModuleNotFoundError: No module named 'rest_framework'`
- `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
1. Make sure you're in the `backend` folder
2. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### ✅ Step 3: Is the Database Set Up?

**Check:** Try running migrations:
```bash
cd backend
venv\Scripts\activate
python manage.py migrate
```

**If you see errors:**
- Run the migrations first
- Make sure you're in the `backend` folder

---

### ✅ Step 4: Is the Admin User Created?

**The backend requires authentication!**

**Check:** Try accessing: `http://localhost:8000/api/history/`

**If you see:**
- "Authentication credentials were not provided" - This is normal, but means you need to create a user

**Solution:**
1. In the backend terminal:
   ```bash
   cd backend
   venv\Scripts\activate
   python manage.py createsuperuser
   ```
2. When prompted:
   - Username: `admin`
   - Email: (press Enter to skip)
   - Password: `admin123`
   - Confirm password: `admin123`

**Important:** The web app uses these credentials:
- Username: `admin`
- Password: `admin123`

If you use different credentials, you'll need to update them in:
- `web-frontend/src/components/UploadComponent.js` (line 53)
- `web-frontend/src/App.js` (line 21)
- `web-frontend/src/components/HistoryPanel.js` (line 9)

---

### ✅ Step 5: Check Browser Console for Errors

**Check:** 
1. Open the web app in your browser (`http://localhost:3000`)
2. Press `F12` to open Developer Tools
3. Click on the "Console" tab
4. Try uploading a file
5. Look for error messages

**Common Errors:**

**Error: "Network Error" or "Failed to fetch"**
- **Cause:** Backend server is not running
- **Fix:** Start the backend server (Step 1)

**Error: "401 Unauthorized"**
- **Cause:** Wrong username/password or user doesn't exist
- **Fix:** Create the admin user (Step 4)

**Error: "CORS policy"**
- **Cause:** CORS configuration issue
- **Fix:** Make sure `django-cors-headers` is installed and configured

**Error: "404 Not Found"**
- **Cause:** API endpoint doesn't exist
- **Fix:** Check that migrations are run and the server is running correctly

---

### ✅ Step 6: Verify Backend API Endpoints

**Test the API directly:**

1. Make sure backend is running
2. Open a new terminal
3. Test the history endpoint:
   ```bash
   curl http://localhost:8000/api/history/ -u admin:admin123
   ```
   
   Or use PowerShell:
   ```powershell
   $cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
   Invoke-WebRequest -Uri "http://localhost:8000/api/history/" -Headers @{Authorization="Basic $cred"}
   ```

**Expected Result:**
- Should return JSON data (even if empty `[]`)
- If you get "401 Unauthorized", create the admin user
- If you get "Connection refused", the backend is not running

---

## Complete Setup Checklist

Before using the web app, make sure:

- [ ] Python 3.8+ is installed
- [ ] Node.js is installed
- [ ] Backend virtual environment is created
- [ ] Backend dependencies are installed (`pip install -r requirements.txt`)
- [ ] Database migrations are run (`python manage.py migrate`)
- [ ] Admin user is created (`python manage.py createsuperuser`)
- [ ] Backend server is running (`python manage.py runserver`)
- [ ] Web frontend dependencies are installed (`npm install` in `web-frontend` folder)
- [ ] Web frontend server is running (`npm start` in `web-frontend` folder)

---

## Common Issues and Solutions

### Issue: "Port 8000 already in use"

**Solution:**
1. Find what's using port 8000:
   ```bash
   netstat -ano | findstr :8000
   ```
2. Kill the process, or use a different port:
   ```bash
   python manage.py runserver 8001
   ```
3. Update API URLs in web-frontend to use port 8001

### Issue: "Cannot activate virtual environment"

**Solution:**
1. Make sure you're in the correct folder
2. Try:
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   ```

### Issue: "pip install fails"

**Solution:**
1. Update pip:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Try installing again:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: "npm install fails"

**Solution:**
1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```
2. Delete `node_modules` and `package-lock.json`
3. Try again:
   ```bash
   npm install
   ```

---

## Step-by-Step Fix for "Upload Failed"

If you're seeing "Upload failed. Please try again.":

1. **Stop everything** (close all terminals)

2. **Start Backend:**
   ```bash
   cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro\backend"
   venv\Scripts\activate
   python manage.py runserver
   ```
   Wait until you see: `Starting development server at http://127.0.0.1:8000/`

3. **Verify Backend is Running:**
   - Open browser: `http://localhost:8000`
   - You should see a Django page (not "This site can't be reached")

4. **Start Web Frontend** (in a NEW terminal):
   ```bash
   cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro\web-frontend"
   npm start
   ```

5. **Test Upload:**
   - Go to `http://localhost:3000`
   - Try uploading `sample_equipment_data.csv`

---

## Still Not Working?

1. **Check Backend Terminal:**
   - Look for error messages when you try to upload
   - Common errors will be displayed there

2. **Check Browser Console:**
   - Press F12 → Console tab
   - Look for red error messages

3. **Verify File Format:**
   - Make sure CSV has these columns:
     - Equipment Name
     - Type
     - Flowrate
     - Pressure
     - Temperature

4. **Check Authentication:**
   - Make sure admin user exists
   - Username: `admin`
   - Password: `admin123`

---

## Quick Test Commands

**Test Backend:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
# Should see: Starting development server at http://127.0.0.1:8000/
```

**Test Web Frontend:**
```bash
cd web-frontend
npm start
# Should open browser to http://localhost:3000
```

**Test API Endpoint:**
Open browser: `http://localhost:8000/api/history/`
- Should ask for username/password
- Use: `admin` / `admin123`
- Should return JSON (even if empty `[]`)
