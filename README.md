# LifeFlow - Blood Donation Management System

A comprehensive web-based Blood Donation Management System built with **Flask**, **MySQL**, and **Jinja2** templates. It manages donors, recipients, blood stock inventory, donation records, and generates monthly/yearly reports.

## Features

- 🔐 Role-based authentication (Admin, Staff, User)
- 🩸 Donor registration & profile management
- 🏥 Recipient management
- 🧪 Blood stock inventory tracking
- 📊 Dashboard analytics & charts
- 📄 Monthly & yearly report generation
- ➕ Blood request submission

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 templates)
- **Auth**: Flask sessions + Werkzeug password hashing

## Project Structure

```
Lifeflow/
├── backend/
│   └── app.py               # Flask application
├── database/
│   └── schema.sql            # Database schema + sample data
├── static/
│   └── js/                  # Frontend JS (charts, validation)
├── templates/               # Jinja2 HTML templates
├── .env.example             # Environment variable template
├── Procfile                 # Deployment config
├── requirements.txt
└── README.md
```

## Setup (Local Development)

### 1. Prerequisites
- Python 3.8+
- MySQL Server 8.0+

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=blood_donation
SECRET_KEY=a_long_random_string
JWT_SECRET_KEY=another_random_string
```

### 5. Set up the database
```bash
mysql -u your_user -p < database/schema.sql
```

### 6. Run the application
```bash
python backend/app.py
```
Visit `http://127.0.0.1:5000` in your browser.

## Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment instructions (local production, cloud, and troubleshooting).

Quick production start with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "backend.app:app"
```

## Security Notes

- Never commit your real `.env` file (it is git-ignored).
- Use a strong `SECRET_KEY` in production.
- The Flask development server is for development only — use Gunicorn/Waitress in production.
