# Quick Start Guide - Step by Step

Follow these steps to run the Chemical Equipment Parameter Visualizer on your computer.

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Node.js 14 or higher installed
- ✅ pip (comes with Python)

To check:
```bash
python --version
node --version
npm --version
```

---

## Step 1: Set Up the Backend (Django API)

### 1.1 Open Terminal/Command Prompt
Navigate to the project folder:
```bash
cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro"
```

### 1.2 Go to Backend Folder
```bash
cd backend
```

**⚠️ IMPORTANT: Make sure you're in the `backend` folder before proceeding!**

You should see something like:
```
C:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro\backend>
```

### 1.3 Create Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

### 1.4 Install Python Packages
**Make sure you're still in the `backend` folder!**

```bash
pip install -r requirements.txt
```

This will install:
- Django
- Django REST Framework
- Pandas
- ReportLab
- django-cors-headers

### 1.5 Set Up Database
```bash
python manage.py migrate
```

### 1.6 Create Admin User (REQUIRED - Do NOT skip this!)
**⚠️ IMPORTANT: You MUST create the admin user, otherwise you'll get "401 Unauthorized" errors!**

**Option A - Quick Script (Recommended):**
Double-click `create_admin_user.bat` in the project root folder.

**Option B - Manual:**
```bash
python manage.py createsuperuser
```
When prompted:
- Username: `admin`
- Email: (press Enter to skip)
- Password: `admin123` (or your choice)
- Confirm password: `admin123` (or your choice)

**Note:** The web app is hardcoded to use `admin` / `admin123`. If you use different credentials, you'll need to update the code.

### 1.7 Start the Backend Server
```bash
python manage.py runserver
```

**✅ Keep this terminal window open!** You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Step 2: Set Up the Web Frontend (React App)

### 2.1 Open a NEW Terminal/Command Prompt
Navigate to the project folder again:
```bash
cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro"
```

### 2.2 Go to Web Frontend Folder
```bash
cd web-frontend
```

### 2.3 Install Node Packages
```bash
npm install
```

This may take a few minutes. It will install:
- React
- Chart.js
- Axios
- and other dependencies

### 2.4 Start the React Development Server
```bash
npm start
```

**✅ Keep this terminal window open!** 

The browser should automatically open to `http://localhost:3000`

If it doesn't, manually open your browser and go to: `http://localhost:3000`

---

## Step 3: Set Up the Desktop App (PyQt5) - Optional

### 3.1 Open a NEW Terminal/Command Prompt
Navigate to the project folder:
```bash
cd "c:\Users\Sweta Kumari\OneDrive\New folder\Catalyst Analytics pro"
```

### 3.2 Go to Desktop App Folder
```bash
cd desktop-app
```

### 3.3 Create Virtual Environment (Optional but Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.4 Install Python Packages
```bash
pip install -r requirements.txt
```

This will install:
- PyQt5
- Matplotlib
- Requests

### 3.5 Run the Desktop Application
**Make sure the backend server is running first!**

```bash
python main.py
```

The desktop application window should open.

---

## How to Use

### Web Application (http://localhost:3000)

1. **Upload CSV File:**
   - Click on "Upload" tab
   - Drag and drop `sample_equipment_data.csv` (in the project root) or click to browse
   - Wait for processing

2. **View Dashboard:**
   - After upload, go to "Dashboard" tab
   - See statistics and charts

3. **Browse Data:**
   - Go to "Data Table" tab
   - Search and sort the data

4. **View History:**
   - Go to "History" tab
   - See previous uploads
   - Download PDF reports

### Desktop Application

1. **Upload CSV:**
   - Click "Upload" in sidebar
   - Click "Browse and Upload CSV"
   - Select your CSV file

2. **View Dashboard:**
   - Click "Dashboard" in sidebar
   - See charts and statistics

3. **Browse Data:**
   - Click "Data Table" in sidebar
   - Search through the data

4. **View History:**
   - Click "History" in sidebar
   - Double-click any item to view it

---

## Troubleshooting

**⚠️ IMPORTANT: If you see "Upload failed. Please try again." error, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.**

### Backend Issues

**Problem:** `ModuleNotFoundError` or import errors
**Solution:** Make sure virtual environment is activated and packages are installed:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use
**Solution:** Kill the process using port 8000 or use a different port:
```bash
python manage.py runserver 8001
```
Then update API URLs in web-frontend and desktop-app to use port 8001.

### Web Frontend Issues

**Problem:** `npm install` fails
**Solution:** 
- Make sure Node.js is installed: `node --version`
- Try clearing cache: `npm cache clean --force`
- Delete `node_modules` folder and `package-lock.json`, then run `npm install` again

**Problem:** Can't connect to backend
**Solution:** 
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify backend URL in `App.js` is `http://localhost:8000`

### Desktop App Issues

**Problem:** PyQt5 installation fails
**Solution:** 
- On Windows, you might need Visual C++ Redistributable
- Try: `pip install --upgrade pip` then `pip install PyQt5`
- On Mac, you might need: `brew install pyqt5`

**Problem:** App can't connect to backend
**Solution:** 
- Make sure backend is running
- Check `API_BASE_URL` in `main.py` is `http://localhost:8000`

---

## Running Order

**Important:** Always start in this order:

1. **First:** Start the Backend (Step 1.7)
2. **Second:** Start the Web Frontend (Step 2.4)
3. **Third (Optional):** Start the Desktop App (Step 3.5)

---

## Sample Data

A sample CSV file (`sample_equipment_data.csv`) is provided in the project root. You can use this to test the application.

The CSV should have these columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

---

## Stopping the Servers

To stop any server:
- Press `Ctrl + C` in the terminal where it's running

---

## Need Help?

If you encounter any issues:
1. Check that all prerequisites are installed
2. Make sure virtual environments are activated
3. Verify all packages are installed correctly
4. Check that ports 3000 and 8000 are not in use by other applications
5. Review the error messages in the terminal/console
