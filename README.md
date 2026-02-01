# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

A hybrid application that runs both as a **Web Application** and a **Desktop Application**, built for data visualization and analytics for chemical equipment. One Django backend serves both React (Web) and PyQt5 (Desktop) frontends.

---

## Project Overview

Users can upload a CSV file containing chemical equipment data (Equipment Name, Type, Flowrate, Pressure, Temperature). The Django backend parses the data, performs analysis using Pandas, and exposes a REST API. Both frontends consume this API to display:

- **Data tables** (searchable, sortable)
- **Charts** (equipment type distribution, Flowrate vs Pressure)
- **Summary statistics** (total count, averages)
- **History** of last 5 uploads
- **PDF report** generation

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend (Web)** | React.js + Chart.js | Table + charts |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Same visualization on desktop |
| **Backend** | Python Django + Django REST Framework | Common backend API |
| **Data Handling** | Pandas | Reading CSV & analytics |
| **Database** | SQLite | Store last 5 uploaded datasets |
| **Version Control** | Git & GitHub | Collaboration & submission |

---

## Project Structure

```
.
├── backend/                      # Django REST API
│   ├── config/                   # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── equipment/                # App: models, views, serializers
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── requirements.txt
│   └── create_admin.py           # Creates admin user (admin/admin123)
│
├── web-frontend/                 # React + Chart.js
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/           # Upload, Dashboard, DataTable, History
│   │   │   ├── UploadComponent.js
│   │   │   ├── Dashboard.js
│   │   │   ├── DataTable.js
│   │   │   └── HistoryPanel.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── package-lock.json
│
├── desktop-app/                  # PyQt5 + Matplotlib
│   ├── main.py
│   └── requirements.txt
│
├── sample_equipment_data.csv     # Sample CSV for demo & testing
├── .gitignore
├── README.md                     # This file – setup instructions
```

---

## Key Features

- **CSV Upload** – Web and Desktop both allow uploading CSV to the backend
- **Data Summary API** – Returns total count, averages (Flowrate, Pressure, Temperature), equipment type distribution
- **Visualization** – Chart.js (Web) and Matplotlib (Desktop): bar charts, scatter plots
- **History Management** – Last 5 uploaded datasets stored in SQLite with summary
- **PDF Report** – Generate PDF report from analyzed data (ReportLab)
- **Basic Authentication** – API endpoints secured with HTTP Basic Auth
- **Sample Data** – Use `sample_equipment_data.csv` for demo and testing

---

## Prerequisites

- **Python 3.8+** (for backend and desktop app)
- **Node.js 14+** and **npm** (for web frontend)
- **pip** (Python package manager)

Check versions:
```bash
python --version
node --version
npm --version
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sweta123761/Chemical-Equipment-Parameter-Visualizer
cd chemical-equipment-visualizer
```

---

### 2. Backend (Django API) – First-Time Setup

Do this **once** after cloning (or when setting up on a new machine).

**Step 1 – Go to backend folder**
```bash
cd backend
```

**Step 2 – Create virtual environment**
```bash
python -m venv venv
```
- **Windows:** `venv\Scripts\activate`  
- **Mac/Linux:** `source venv/bin/activate`  
You should see `(venv)` in your prompt.

**Step 3 – Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 – Create database tables**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Step 5 – Create admin user (required for API auth)**  
The API uses Basic Authentication. The web and desktop apps send username `admin` and password `admin123`. You must create this user once:
```bash
python create_admin.py
```
This creates user **admin** with password **admin123**. (Alternatively use `python manage.py createsuperuser` and set the same credentials.)

---

### 3. Starting the Backend (Every Time You Run the App)

Use **Terminal 1** (Command Prompt or PowerShell):

```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

- **Backend URL:** http://localhost:8000  
- **Keep this terminal open** while using the web or desktop app.  
- To stop: press `Ctrl+C`.

---

### 4. Web Frontend (React) – First-Time Setup

Do this **once** after cloning.

**Step 1 – Go to web frontend folder** (in a **new** terminal)
```bash
cd web-frontend
```

**Step 2 – Install dependencies**
```bash
npm install
```

---

### 5. Starting the Web Frontend (Every Time You Run the App)

Use **Terminal 2** (backend must already be running in Terminal 1):

```bash
cd web-frontend
npm start
```

**You should see:**
```
Compiled successfully!
Local: http://localhost:3000
```

- **Web app URL:** http://localhost:3000  
- The browser usually opens automatically.  
- To stop: press `Ctrl+C` in that terminal.

**If you see "Proxy error" or "ECONNREFUSED":** the backend is not running. Start the backend first (see section 3), then run `npm start` again.

---

### 6. Desktop Frontend (PyQt5) 

**First-time setup (once):**
```bash
cd desktop-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**To run the desktop app:**  
Backend must be running. In a new terminal:
```bash
cd desktop-app
venv\Scripts\activate
python main.py
```

Uses the same API credentials: **admin** / **admin123**.

---

### 7. Quick Reference – Starting Backend and Frontend

| Order | Where | Command | What you see |
|-------|--------|---------|----------------|
| 1 | **Terminal 1** | `cd backend` → `venv\Scripts\activate` → `python manage.py runserver` | `Starting development server at http://127.0.0.1:8000/` |
| 2 | **Terminal 2** | `cd web-frontend` → `npm start` | `Compiled successfully!` and browser at http://localhost:3000 |

**API credentials (used by both frontends):** Username: **admin** | Password: **admin123**

---

## API Endpoints

All endpoints require **HTTP Basic Authentication** (username: `admin`, password: `admin123`).

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload CSV file; returns summary + raw data |
| GET | `/api/history/` | Last 5 uploads with summary |
| GET | `/api/report/?id=<upload_id>` | Download PDF report for an upload |

---

## Sample Data

Use **`sample_equipment_data.csv`** in the project root for demo and testing.

Required CSV columns:

- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  

---

## Running Order

1. **Start Backend first** (Terminal 1): `cd backend` → activate venv → `python manage.py runserver`
2. **Then start Web** (Terminal 2): `cd web-frontend` → `npm start`
3. **Desktop** : Backend must be running; then `cd desktop-app` → activate venv → `python main.py`

See **Quick Reference** in Setup Instructions (section 7) for the exact commands.


## Troubleshooting

| Issue | Solution |
|-------|----------|
| **"no such table: equipment_equipmentupload"** | In `backend/`: run `python manage.py makemigrations` then `python manage.py migrate`. |
| **401 Unauthorized** | Create admin user: in `backend/` run `python create_admin.py` (creates `admin` / `admin123`) or `python manage.py createsuperuser` and use the same credentials. |
| **Proxy error / ECONNREFUSED** | Backend is not running. Start it first: `cd backend`, activate venv, then `python manage.py runserver`. |
| **Port 8000 or 3000 in use** | Stop the other app using that port, or run backend on another port: `python manage.py runserver 8001` (then update API URL in web/desktop if needed). |
| **"npm is not recognized"** | Install Node.js from https://nodejs.org/ and restart the terminal. |
| **Frontend blank or won’t start** | In `web-frontend/` run `npm install` then `npm start`. If it still fails, delete `node_modules` and `package-lock.json`, run `npm install` again. |
| **Upload failed in web app** | Ensure backend is running on port 8000 and admin user exists with password `admin123`. |
| **Permission denied when creating venv** | A partial `venv` folder may exist. Delete it: `rmdir /s /q venv` (Windows) in `backend/`, then run `python -m venv venv` again. If the project is in OneDrive, pause OneDrive sync or create venv outside the synced folder. |

---

## License

This project was developed as an internship screening task.

---

## Author

Developed for the Intern Screening Task – Hybrid Web + Desktop Application.
