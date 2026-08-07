# LifeFlow Deployment Guide

This guide covers how to deploy the LifeFlow Blood Donation Management System.

## ✅ Verified Working Status

The application has been verified to work correctly with the current setup:

| Component | Status |
|-----------|--------|
| MySQL server (MySQL90) | ✅ Running |
| Database `blood_donation` | ✅ Created (10 tables, 4 routines) |
| Flask server | ✅ Starts on `http://127.0.0.1:5000` |
| `/login` page | ✅ HTTP 200 |
| Admin login (`admin` / `admin123`) | ✅ Success → redirects to `/dashboard` |
| `/dashboard` page | ✅ HTTP 200 |
| `/api/dashboard/stats` | ✅ Returns 13 donors, 15 recipients, 284 units |
| `/donors` page | ✅ HTTP 200 |

**Login credentials:**
- **Admin**: username `admin`, password `admin123`
- **Staff**: username `staff` (password unknown - reset via script if needed)
- Existing users: `Nirrmam`, `Nirmam`, `admin1`, `Siddarth`

---

## Option A: Local Deployment (Development)

### 1. Prerequisites
- Python 3.8+
- MySQL Server 8.0+ (already installed as MySQL90)
- Git (for cloning)

### 2. Install Dependencies
```bash
cd d:/Desktop/Projects/Lifeflow

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# Windows PowerShell:
venv\Scripts\Activate.ps1
# or Windows CMD:
venv\Scripts\activate.bat

# Install requirements
pip install -r requirements.txt
```

> **⚠️ NOTE:** The existing `venv` folder is **broken**. It was created with Python 3.13
> (`C:\Users\Nirmam\AppData\Local\Programs\Python\Python313\python.exe`), which has been
> uninstalled. If you want to use a virtual environment, delete the old `venv` folder and
> recreate it with your current Python (3.14):
> ```bash
> Remove-Item -Recurse -Force venv
> python -m venv venv
> venv\Scripts\Activate.ps1
> pip install -r requirements.txt
> ```

### 3. Configure Environment Variables
Create a `.env` file in the project root (or update the existing one):
```
DB_HOST=localhost
DB_USER=Nirrmam
DB_PASSWORD=lifeflow
DB_NAME=blood_donation
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-super-secret-jwt-key
```

> **⚠️ NOTE:** The database credentials are currently **hardcoded** in `backend/app.py`
> (lines for `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`). The app reads `.env` via
> `load_dotenv()` but the DB config does NOT currently use environment variables. For a
> cleaner setup, modify `app.py` to read from env vars:
> ```python
> DB_HOST = os.environ.get('DB_HOST', 'localhost')
> DB_USER = os.environ.get('DB_USER', 'root')
> DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
> DB_NAME = os.environ.get('DB_NAME', 'blood_donation')
> ```

### 4. Set Up the Database
```bash
# If schema is not yet loaded:
mysql -u Nirrmam -plifeflow < database/schema.sql
```

### 5. Run the Application
```bash
python backend/app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## Option B: Production Deployment

The Flask development server (`app.run(debug=True)`) is **NOT** suitable for production.
Use a production WSGI server instead.

### Using Gunicorn (Linux/macOS)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "backend.app:app"
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --host 0.0.0.0 --port 8000 "backend.app:app"
```

### Using a Reverse Proxy (Nginx + Gunicorn)
Create `/etc/nginx/sites-available/lifeflow`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Important Production Changes
1. **Disable debug mode** — change `app.run(debug=True)` to run via WSGI server.
2. **Use strong secrets** — set strong `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`.
3. **Use environment variables** for DB credentials (don't hardcode).
4. **Set up HTTPS** using Let's Encrypt / Certbot.
5. **Run as a service** using systemd (Linux) or Windows Service (NSSM).

---

## Option C: Cloud Deployment

### Render / Railway / Heroku
1. Push code to a GitHub repository.
2. Create a MySQL database (e.g., ClearDB, JawsDB, Railway MySQL).
3. Set environment variables (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY).
4. Deploy with a `Procfile`:
   ```
   web: gunicorn "backend.app:app"
   ```
5. Set the build command to `pip install -r requirements.txt`.

### AWS / Google Cloud / Azure
1. Launch a VM instance.
2. Install Python, MySQL, and Nginx.
3. Follow "Option B" for reverse proxy setup.
4. Use systemd to keep the app running.

---

## Troubleshooting

### Database connection errors
- Verify MySQL is running: `Get-Service | Where-Object {$_.Name -like '*mysql*'}`
- Verify credentials: `mysql -u Nirrmam -plifeflow -e "SHOW DATABASES;"`
- Run the schema if the database is empty.

### "Module not found: mysql"
Install the connector: `pip install mysql-connector-python`

### Port 5000 already in use
Change the port in `app.run()` or use a different WSGI port.

### venv broken (Python 3.13 missing)
Recreate the venv with your current Python (see Step 2 note above).

---

## Project Structure
```
Lifeflow/
├── backend/
│   └── app.py
├── database/
│   └── schema.sql
├── static/
│   └── js/
│       ├── dashboard_charts.js
│       └── profile-validation.js
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── dashboard.html
│   └── ... (all HTML templates)
├── venv/          (broken - recreate)
├── .env
├── requirements.txt
└── README.md
