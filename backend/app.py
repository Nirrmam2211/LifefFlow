import os
from datetime import timedelta, date
from urllib.parse import urlparse
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- App Initialization ---
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- Configuration ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-super-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-super-secret-jwt-key')
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
app.config["DEBUG_MODE"] = os.environ.get("FLASK_DEBUG", "0") == "1"

# --- Database Configuration ---
def _first_non_empty(*values, default=None):
    """Return the first value that is not None and not an empty string."""
    for value in values:
        if value is not None and value != '':
            return value
    return default


def get_db_config():
    """Dynamically parses and returns database connection parameters."""
    # --- DEBUG: dump the raw environment variables we care about ---
    _debug_env_vars = [
        'MYSQL_URL', 'DATABASE_URL', 'MYSQL_PRIVATE_URL', 'DATABASE_PUBLIC_URL',
        'MYSQL_PUBLIC_URL', 'DB_HOST', 'MYSQLHOST', 'MYSQL_HOST', 'DB_PORT',
        'MYSQLPORT', 'MYSQL_PORT', 'DB_USER', 'MYSQLUSER', 'MYSQL_USER',
        'DB_PASSWORD', 'MYSQLPASSWORD', 'MYSQL_PASSWORD', 'DB_NAME',
        'MYSQLDATABASE', 'MYSQL_DATABASE'
    ]
    print("=" * 60, flush=True)
    print("[DB CONFIG DEBUG] Raw environment variables (before parsing):", flush=True)
    for var_name in _debug_env_vars:
        raw_value = os.environ.get(var_name)
        if raw_value is not None and 'PASSWORD' in var_name:
            display_value = f"<set, length={len(raw_value)}>"
        elif raw_value is None:
            display_value = "<NOT SET>"
        else:
            display_value = raw_value
        print(f"[DB CONFIG DEBUG]   {var_name} = {display_value}", flush=True)

    db_url = (
        os.environ.get('MYSQL_URL') or 
        os.environ.get('DATABASE_URL') or 
        os.environ.get('MYSQL_PRIVATE_URL') or
        os.environ.get('DATABASE_PUBLIC_URL') or
        os.environ.get('MYSQL_PUBLIC_URL')
    )
    if db_url:
        _which_url_var = next(
            (name for name in ('MYSQL_URL', 'DATABASE_URL', 'MYSQL_PRIVATE_URL', 'DATABASE_PUBLIC_URL', 'MYSQL_PUBLIC_URL')
             if os.environ.get(name)),
            None
        )
        print(f"[DB CONFIG DEBUG] Using connection URL from {_which_url_var}", flush=True)
    else:
        print("[DB CONFIG DEBUG] No connection URL env var found (MYSQL_URL/DATABASE_URL/etc. all unset/empty)", flush=True)

    host = _first_non_empty(
        os.environ.get('DB_HOST'),
        os.environ.get('MYSQLHOST'),
        os.environ.get('MYSQL_HOST'),
        default='localhost'
    )
    port_value = _first_non_empty(
        os.environ.get('DB_PORT'),
        os.environ.get('MYSQLPORT'),
        os.environ.get('MYSQL_PORT'),
        default=3306
    )
    try:
        port = int(port_value)
    except (TypeError, ValueError):
        port = 3306
    user = _first_non_empty(
        os.environ.get('DB_USER'),
        os.environ.get('MYSQLUSER'),
        os.environ.get('MYSQL_USER'),
        default='root'
    )
    password = _first_non_empty(
        os.environ.get('DB_PASSWORD'),
        os.environ.get('MYSQLPASSWORD'),
        os.environ.get('MYSQL_PASSWORD'),
        default=''
    )
    database = _first_non_empty(
        os.environ.get('DB_NAME'),
        os.environ.get('MYSQLDATABASE'),
        os.environ.get('MYSQL_DATABASE'),
        default='blood_donation'
    )

    print(
        f"[DB CONFIG DEBUG] After individual-var resolution (before URL override): "
        f"host={host}, port={port}, user={user}, password={'<set>' if password else '<empty>'}, database={database}",
        flush=True
    )

    if db_url and 'mysql' in db_url:
        try:
            parsed = urlparse(db_url)
            print(f"[DB CONFIG DEBUG] Parsing connection URL: scheme={parsed.scheme}, "
                  f"hostname={parsed.hostname}, port={parsed.port}, username={parsed.username}, "
                  f"password={'<set>' if parsed.password else '<empty>'}, path={parsed.path}", flush=True)
            if parsed.hostname: host = parsed.hostname
            if parsed.port: port = int(parsed.port)
            if parsed.username: user = parsed.username
            if parsed.password: password = parsed.password
            if parsed.path and len(parsed.path) > 1:
                database = parsed.path.lstrip('/')
        except Exception as e:
            print(f"[DB CONFIG DEBUG] Error parsing database URL: {e}", flush=True)
    else:
        print("[DB CONFIG DEBUG] Skipping URL parsing (no URL, or URL does not contain 'mysql')", flush=True)

    print(
        f"[DB CONFIG DEBUG] FINAL config -> host={host}, port={port}, user={user}, "
        f"password={'<set>' if password else '<empty>'}, database={database}",
        flush=True
    )
    print("=" * 60, flush=True)

    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database
    }

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    config = get_db_config()
    print(
        f"[DB CONNECT DEBUG] Attempting connection with host={config['host']}, "
        f"port={config['port']}, user={config['user']}, database={config['database']}, "
        f"password={'<set>' if config['password'] else '<empty>'}",
        flush=True
    )
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            connect_timeout=10
        )
        print(f"[DB CONNECT DEBUG] Successfully connected to {config['host']}:{config['port']}", flush=True)
        return conn
    except mysql.connector.Error as err:
        print(
            f"[DB CONNECT DEBUG] Connection failed with host={config['host']}, "
            f"port={config['port']}, user={config['user']}, database={config['database']}: {err}",
            flush=True
        )
        # If database doesn't exist yet, try creating it
        if err.errno == 1049: # Unknown database
            try:
                temp_conn = mysql.connector.connect(
                    host=config['host'],
                    port=config['port'],
                    user=config['user'],
                    password=config['password'],
                    connect_timeout=10
                )
                cur = temp_conn.cursor()
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{config['database']}`")
                cur.close()
                temp_conn.close()
                return mysql.connector.connect(
                    host=config['host'],
                    port=config['port'],
                    user=config['user'],
                    password=config['password'],
                    database=config['database'],
                    connect_timeout=10
                )
            except Exception as create_err:
                _record_db_error(
                    f"Failed to auto-create database {config['database']}: {create_err}"
                )
                return None
        _record_db_error(
            f"DATABASE CONNECTION ERROR (host={config['host']}, port={config['port']}, user={config['user']}, db={config['database']}): {err}"
        )
        return None

_db_initialized = False
LAST_DB_ERROR = None


def _record_db_error(message):
    """Store and log the latest database error for troubleshooting."""
    global LAST_DB_ERROR
    LAST_DB_ERROR = message
    app.logger.error(message)

def init_db():
    """Initializes the database schema if tables do not exist."""
    global _db_initialized
    conn = get_db_connection()
    if conn is None:
        print("WARNING: Could not connect to database for initialization.")
        return False
    cursor = conn.cursor()
    try:
        # Create Blood_Bank
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Blood_Bank (
                bank_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                address VARCHAR(200),
                contact VARCHAR(100)
            )
        """)
        # Create Donor
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Donor (
                donor_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                age INT,
                gender CHAR(1),
                blood_group VARCHAR(5),
                contact VARCHAR(20),
                address VARCHAR(255),
                email VARCHAR(100) UNIQUE,
                last_donation_date DATE,
                eligibility_status VARCHAR(30)
            )
        """)
        # Create Recipient
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recipient (
                recipient_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                age INT,
                gender CHAR(1),
                blood_group_needed VARCHAR(5),
                contact VARCHAR(20),
                address VARCHAR(255),
                medical_notes VARCHAR(255),
                registration_date DATE
            )
        """)
        # Create Blood_Stock
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Blood_Stock (
                unit_id INT PRIMARY KEY AUTO_INCREMENT,
                blood_group VARCHAR(5),
                quantity INT,
                collection_date DATE,
                expiry_date DATE,
                storage_location VARCHAR(50),
                bank_id INT,
                FOREIGN KEY (bank_id) REFERENCES Blood_Bank(bank_id) ON DELETE SET NULL
            )
        """)
        # Create Donation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Donation (
                donation_id INT PRIMARY KEY AUTO_INCREMENT,
                donor_id INT,
                unit_id INT,
                donation_date DATE,
                quantity INT,
                FOREIGN KEY (donor_id) REFERENCES Donor(donor_id) ON DELETE SET NULL,
                FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id) ON DELETE SET NULL
            )
        """)
        # Create Blood_Issue
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Blood_Issue (
                issue_id INT PRIMARY KEY AUTO_INCREMENT,
                recipient_id INT,
                unit_id INT,
                issue_date DATE,
                hospital VARCHAR(100),
                quantity INT,
                FOREIGN KEY (recipient_id) REFERENCES Recipient(recipient_id) ON DELETE SET NULL,
                FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id) ON DELETE SET NULL
            )
        """)
        # Create User
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE,
                password_hash VARCHAR(255),
                role ENUM('admin', 'staff', 'user') DEFAULT 'user',
                created_at DATE,
                donor_id INT,
                FOREIGN KEY (donor_id) REFERENCES Donor(donor_id) ON DELETE SET NULL
            )
        """)
        # Create Blood_Request
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Blood_Request (
                request_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                blood_group VARCHAR(5) NOT NULL,
                units_needed INT NOT NULL,
                hospital VARCHAR(255) NOT NULL,
                urgency_level VARCHAR(50) NOT NULL,
                contact_info VARCHAR(50) NOT NULL,
                status VARCHAR(30) DEFAULT 'Pending',
                request_date DATE,
                FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
            )
        """)
        # Create Monthly_Donation_Report
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Monthly_Donation_Report (
                report_id INT PRIMARY KEY AUTO_INCREMENT,
                year INT,
                month INT,
                total_donations INT,
                total_quantity INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY year_month_unique (year, month)
            )
        """)
        # Create Yearly_Donation_Report
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Yearly_Donation_Report (
                report_id INT PRIMARY KEY AUTO_INCREMENT,
                year INT UNIQUE,
                total_donations INT,
                total_quantity INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # Seed sample blood banks and admin user if empty
        cursor.execute("SELECT COUNT(*) FROM User WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            admin_pwd = generate_password_hash("admin123")
            cursor.execute(
                "INSERT INTO User (username, password_hash, role, created_at) VALUES (%s, %s, 'admin', %s)",
                ("admin", admin_pwd, date.today())
            )
            conn.commit()
            print("Default admin account created: username='admin', password='admin123'")

        cursor.execute("SELECT COUNT(*) FROM Blood_Bank")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Blood_Bank (name, address, contact) VALUES
                ('Central Blood Bank', '123 Main St, City', '123-456-7890'),
                ('Westside Blood Bank', '456 West St, City', '987-654-3210'),
                ('Eastside Blood Center', '789 East Blvd, City', '321-654-0987')
            """)
            conn.commit()

        _db_initialized = True
        print("Database schema initialized successfully.")
        return True
    except Exception as err:
        _record_db_error(f"Database initialization error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Auto-initialize database schema on startup
try:
    init_db()
except Exception as e:
    print(f"Failed to auto-initialize database on startup: {e}")

@app.before_request
def ensure_db_ready():
    global _db_initialized
    if not _db_initialized and not request.path.startswith('/static'):
        init_db()

@app.route('/api/db-status')
def db_status():
    config = get_db_config()
    conn = get_db_connection()
    if conn is None:
        return jsonify({
            'status': 'error',
            'message': 'Failed to connect to MySQL database.',
            'last_error': LAST_DB_ERROR,
            'configured_host': config['host'],
            'configured_port': config['port'],
            'configured_user': config['user'],
            'configured_database': config['database']
        }), 500
    try:
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify({
            'status': 'connected',
            'database': config['database'],
            'host': config['host'],
            'tables': tables
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --- Helper Functions ---
def query_db(query, args=(), one=False):
    """Executes a database query."""
    conn = get_db_connection()
    if conn is None: return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, args)
        # For SELECT queries, fetch results
        if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESC')):
            results = cursor.fetchall()
            return (results[0] if results else None) if one else results
        # For INSERT, UPDATE, DELETE, commit changes
        else:
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    except mysql.connector.Error as err:
        _record_db_error(f"DATABASE QUERY ERROR: {err}")
        conn.rollback() # Roll back in case of error
        return None
    finally:
        cursor.close()
        conn.close()


# --- Authentication Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = 'user'
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))

        user_exists = query_db('SELECT * FROM User WHERE username = %s', [username], one=True)
        if user_exists:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        res = query_db('INSERT INTO User (username, password_hash, role, created_at, donor_id) VALUES (%s, %s, %s, %s, NULL)',
                 (username, hashed_password, role, date.today()))

        if res is None:
            if LAST_DB_ERROR:
                flash(f'Database error: {LAST_DB_ERROR}', 'danger')
            else:
                flash('Database error: Unable to create account. Please check your database connection.', 'danger')
            return redirect(url_for('register'))

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return redirect(url_for('login'))

        user = query_db('SELECT * FROM User WHERE username = %s', [username], one=True)

        if user and check_password_hash(user['password_hash'], password):
            session.permanent = True
            session['user'] = user['username']
            session['role'] = user['role']
            flash('Logged in successfully!', 'success')

            if user['role'] in ['admin', 'staff']:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Admin/Staff Dashboard ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# --- User Dashboard ---
@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('user_dashboard.html')

# --- API Routes for Admin Dashboard ---
@app.route('/api/dashboard/stats')
def dashboard_stats():
    if 'user' not in session: return jsonify({'error': 'Unauthorized'}), 401
    total_donors = query_db('SELECT COUNT(*) as count FROM Donor', one=True)['count']
    total_recipients = query_db('SELECT COUNT(*) as count FROM Recipient', one=True)['count']
    units_available = query_db('SELECT SUM(quantity) as count FROM Blood_Stock', one=True)['count'] or 0
    return jsonify({'total_donors': total_donors, 'total_recipients': total_recipients, 'units_available': units_available})

@app.route('/api/reports/monthly/<int:year>/<int:month>')
def get_monthly_report(year, month):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Generate the report first
    query_db('CALL generate_monthly_report(%s, %s)', (year, month))
    
    # Get the report data
    report = query_db('SELECT * FROM Monthly_Donation_Report WHERE year = %s AND month = %s', 
                     (year, month), one=True)
    
    if not report:
        return jsonify({'error': 'No data found for the specified period'}), 404
        
    # Format for text file
    text_content = f"""Monthly Donation Report
Year: {report['year']}
Month: {report['month']}
Total Donations: {report['total_donations']}
Total Quantity: {report['total_quantity']}
Generated on: {report['created_at']}
"""
    return jsonify({'content': text_content})

@app.route('/api/reports/yearly/<int:year>')
def get_yearly_report(year):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Generate the report first
    query_db('CALL generate_yearly_report(%s)', [year])
    
    # Get the report data
    report = query_db('SELECT * FROM Yearly_Donation_Report WHERE year = %s', [year], one=True)
    
    if not report:
        return jsonify({'error': 'No data found for the specified year'}), 404
        
    # Format for text file
    text_content = f"""Yearly Donation Report
Year: {report['year']}
Total Donations: {report['total_donations']}
Total Quantity: {report['total_quantity']}
Generated on: {report['created_at']}
"""
    return jsonify({'content': text_content})

@app.route('/api/dashboard/blood_stock')
def blood_stock_data():
    if 'user' not in session: return jsonify({'error': 'Unauthorized'}), 401
    stock = query_db("SELECT blood_group, SUM(quantity) as total_units FROM Blood_Stock GROUP BY blood_group")
    return jsonify(stock)


@app.route('/reports')
def reports_page():
    # Admin/staff only
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))

    monthly = query_db('SELECT * FROM Monthly_Donation_Report ORDER BY year DESC, month DESC') or []
    yearly = query_db('SELECT * FROM Yearly_Donation_Report ORDER BY year DESC') or []
    return render_template('reports.html', monthly_reports=monthly, yearly_reports=yearly)


@app.route('/reports/download/monthly/<int:year>/<int:month>')
def download_monthly_report(year, month):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))

    # Ensure report exists / is generated
    query_db('CALL generate_monthly_report(%s, %s)', (year, month))
    report = query_db('SELECT * FROM Monthly_Donation_Report WHERE year = %s AND month = %s', (year, month), one=True)
    if not report:
        flash('No report available for the selected month.', 'danger')
        return redirect(url_for('reports_page'))

    text_content = f"""Monthly Donation Report
Year: {report['year']}
Month: {report['month']}
Total Donations: {report['total_donations']}
Total Quantity: {report['total_quantity']}
Generated on: {report['created_at']}
"""
    resp = make_response(text_content)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    filename = f"monthly_report_{report['year']}_{report['month']:02d}.txt"
    resp.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return resp


@app.route('/reports/download/yearly/<int:year>')
def download_yearly_report(year):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))

    query_db('CALL generate_yearly_report(%s)', [year])
    report = query_db('SELECT * FROM Yearly_Donation_Report WHERE year = %s', [year], one=True)
    if not report:
        flash('No report available for the selected year.', 'danger')
        return redirect(url_for('reports_page'))

    text_content = f"""Yearly Donation Report
Year: {report['year']}
Total Donations: {report['total_donations']}
Total Quantity: {report['total_quantity']}
Generated on: {report['created_at']}
"""
    resp = make_response(text_content)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    filename = f"yearly_report_{report['year']}.txt"
    resp.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return resp


# --- Management Pages (Admin/Staff) ---
@app.route('/donors')
def donors():
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    donor_list = query_db("SELECT * FROM Donor ORDER BY name")
    return render_template('donors.html', donors=donor_list)

@app.route('/donors/edit/<int:donor_id>', methods=['GET', 'POST'])
def edit_donor(donor_id):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        flash('You do not have permission to edit donors.', 'danger')
        return redirect(url_for('login'))
    
    # Get the donor information first
    donor = query_db("SELECT * FROM Donor WHERE donor_id = %s", [donor_id], one=True)
    if not donor:
        flash('Donor not found.', 'danger')
        return redirect(url_for('donors'))
        
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            age = request.form.get('age')
            gender = request.form.get('gender')
            blood_group = request.form.get('blood_group')
            contact = request.form.get('contact')
            email = request.form.get('email')
            address = request.form.get('address')
            last_donation_date = request.form.get('last_donation_date') or None
            eligibility_status = request.form.get('eligibility_status')
            
            # Validate required fields
            if not all([name, age, gender, blood_group, contact, email, address, eligibility_status]):
                flash('All fields except last donation date are required.', 'danger')
                return redirect(url_for('edit_donor', donor_id=donor_id))
            
            # Check if email exists for other donors
            existing_donor = query_db("SELECT * FROM Donor WHERE email = %s AND donor_id != %s", 
                                    [email, donor_id], one=True)
            if existing_donor:
                flash('A donor with this email address already exists.', 'danger')
                return redirect(url_for('edit_donor', donor_id=donor_id))
                
            # Update donor information
            query_db("""UPDATE Donor SET 
                       name = %s, age = %s, gender = %s, blood_group = %s, 
                       contact = %s, address = %s, email = %s, 
                       last_donation_date = %s, eligibility_status = %s 
                       WHERE donor_id = %s""",
                    (name, age, gender, blood_group, contact, address, 
                     email, last_donation_date, eligibility_status, donor_id))
            
            flash('Donor information updated successfully!', 'success')
            return redirect(url_for('donors'))
            
        except Exception as e:
            flash(f'An error occurred while updating donor information: {str(e)}', 'danger')
            return redirect(url_for('edit_donor', donor_id=donor_id))
    
    donor = query_db("SELECT * FROM Donor WHERE donor_id = %s", [donor_id], one=True)
    if not donor:
        flash('Donor not found.', 'danger')
        return redirect(url_for('donors'))
        
    return render_template('edit_donor.html', donor=donor)

@app.route('/donors/add', methods=['GET', 'POST'])
def add_donor():
    if 'user' not in session:
        flash('Please log in to register as a donor.', 'danger')
        return redirect(url_for('login'))
    
    # Check if user is already registered as a donor
    user = query_db("SELECT donor_id FROM User WHERE username = %s", [session.get('user')], one=True)
    if user and user.get('donor_id'):
        return redirect(url_for('user_profile'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            name = request.form.get('name')
            age = request.form.get('age')
            gender = request.form.get('gender')
            blood_group = request.form.get('blood_group')
            contact = request.form.get('contact')
            address = request.form.get('address')
            last_donation_date = request.form.get('last_donation_date') or None
            
            if not all([email, name, age, gender, blood_group, contact, address]):
                flash('All fields except last donation date are required.', 'danger')
                return redirect(url_for('add_donor'))
            
            # Check if email already exists
            existing_donor = query_db("SELECT * FROM Donor WHERE email = %s", [email], one=True)
            if existing_donor:
                flash('A donor with this email address already exists.', 'danger')
                return redirect(url_for('add_donor'))
            
            # Insert new donor
            donor_id = query_db("""INSERT INTO Donor 
                                  (name, age, gender, blood_group, contact, email, address, last_donation_date, eligibility_status) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Eligible')""",
                              (name, age, gender, blood_group, contact, email, address, last_donation_date))
            
            # Link donor to user
            query_db("UPDATE User SET donor_id = %s WHERE username = %s", (donor_id, session.get('user')))
            
            flash('Donor registration successful!', 'success')
            return redirect(url_for('user_profile'))
            
        except Exception as e:
            flash(f'An error occurred while registering as a donor: {str(e)}', 'danger')
            return redirect(url_for('add_donor'))
    
    return render_template('add_donor.html')

@app.route('/donors/delete/<int:donor_id>', methods=['POST'])
def delete_donor_route(donor_id):
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        flash('You do not have permission to delete donors.', 'danger')
        return redirect(url_for('login'))

    try:
        # Delete related records from the Donation table
        query_db("DELETE FROM Donation WHERE donor_id = %s", [donor_id])

        # Delete related records from the User table
        query_db("UPDATE User SET donor_id = NULL WHERE donor_id = %s", [donor_id]) # Set to NULL instead of deleting user

        # Delete the donor record
        query_db("DELETE FROM Donor WHERE donor_id = %s", [donor_id])

        flash('Donor and associated records deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred while deleting donor: {str(e)}', 'danger')
    
    return redirect(url_for('donors'))

@app.route('/recipients')
def recipients():
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    recipient_list = query_db("SELECT * FROM Recipient ORDER BY name")
    return render_template('recipients.html', recipients=recipient_list)

@app.route('/stock')
def stock():
    if 'user' not in session or session.get('role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    stock_list = query_db("SELECT bs.*, bb.name as bank_name FROM Blood_Stock bs LEFT JOIN Blood_Bank bb ON bs.bank_id = bb.bank_id")
    return render_template('stock.html', stock=stock_list)

# --- Blood Request Management ---
@app.route('/request-blood', methods=['GET', 'POST'])
def request_blood():
    if 'user' not in session:
        flash('Please log in to request blood.', 'danger')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            blood_group = request.form.get('blood_group')
            units_needed = request.form.get('units_needed')
            hospital = request.form.get('hospital')
            urgency = request.form.get('urgency')
            contact = request.form.get('contact')
            
            if not all([blood_group, units_needed, hospital, urgency, contact]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('request_blood'))
                
            query_db("""INSERT INTO Blood_Request 
                       (user_id, blood_group, units_needed, hospital, urgency_level, contact_info, status, request_date) 
                       VALUES ((SELECT user_id FROM User WHERE username = %s), %s, %s, %s, %s, %s, 'Pending', CURDATE())""",
                    (session['user'], blood_group, units_needed, hospital, urgency, contact))
                    
            flash('Blood request submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('user_dashboard'))
            
        except Exception as e:
            flash(f'An error occurred while submitting your request: {str(e)}', 'danger')
            return redirect(url_for('request_blood'))
            
    return render_template('request_blood.html')

# --- User-Specific Pages ---
@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    if 'user' not in session:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('login'))
        
    if session.get('role') != 'user':
        flash('Access denied. This page is for donors only.', 'danger')
        return redirect(url_for('login'))
    
    # Get user and donor information
    user = query_db("SELECT user_id, donor_id FROM User WHERE username = %s", [session.get('user')], one=True)
    if not user:
        flash('User account not found.', 'danger')
        return redirect(url_for('login'))
    
    donor_info = None
    if user.get('donor_id'):
        donor_info = query_db("SELECT * FROM Donor WHERE donor_id = %s", [user['donor_id']], one=True)
        
        if request.method == 'POST':
            try:
                # Get and validate form data
                name = request.form.get('name', '').strip()
                age = request.form.get('age', '')
                gender = request.form.get('gender', '')
                blood_group = request.form.get('blood_group', '')
                contact = request.form.get('contact', '').strip()
                email = request.form.get('email', '').strip()
                address = request.form.get('address', '').strip()
                
                # Input validation
                if not name or len(name) < 2:
                    flash('Please enter a valid name (at least 2 characters).', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                    
                try:
                    age = int(age)
                    if age < 18 or age > 65:
                        flash('Age must be between 18 and 65 years.', 'danger')
                        return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                except ValueError:
                    flash('Please enter a valid age.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                
                if gender not in ['M', 'F', 'O']:
                    flash('Please select a valid gender.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                    
                if blood_group not in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
                    flash('Please select a valid blood group.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                    
                if not contact or len(contact) < 10:
                    flash('Please enter a valid contact number.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                    
                if not email or '@' not in email:
                    flash('Please enter a valid email address.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                    
                if not address or len(address) < 10:
                    flash('Please enter a complete address.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                
                # Check if email exists for other donors
                existing_donor = query_db("SELECT * FROM Donor WHERE email = %s AND donor_id != %s", 
                                       [email, user['donor_id']], one=True)
                if existing_donor:
                    flash('This email is already registered with another donor.', 'danger')
                    return render_template('user_profile.html', donor=donor_info, edit_mode=True)
                
                # Update donor information
                query_db("""UPDATE Donor SET 
                           name = %s, age = %s, gender = %s, blood_group = %s,
                           contact = %s, email = %s, address = %s
                           WHERE donor_id = %s""",
                        (name, age, gender, blood_group, contact, email, 
                         address, user['donor_id']))
                
                # Refresh donor info after update
                donor_info = query_db("SELECT * FROM Donor WHERE donor_id = %s", [user['donor_id']], one=True)
                flash('Your profile has been updated successfully!', 'success')
                return redirect(url_for('user_profile'))
                
            except Exception as e:
                app.logger.error(f'Error updating donor profile: {str(e)}')
                flash('An unexpected error occurred. Please try again.', 'danger')
                return render_template('user_profile.html', donor=donor_info, edit_mode=True)
    
    return render_template('user_profile.html', donor=donor_info, edit_mode=request.args.get('edit', False))

@app.route('/user/donations')
def user_donations():
    if 'user' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    user = query_db("SELECT donor_id FROM User WHERE username = %s", [session.get('user')], one=True)
    
    donations = []
    if user and user.get('donor_id'):
        donations = query_db(
            """SELECT d.donation_id, d.donation_date, d.quantity, bb.name as bank_name
               FROM Donation d 
               JOIN Blood_Stock bs ON d.unit_id = bs.unit_id
               JOIN Blood_Bank bb ON bs.bank_id = bb.bank_id
               WHERE d.donor_id = %s 
               ORDER BY d.donation_date DESC""",
            [user['donor_id']]
        )
        
    return render_template('user_donations.html', donations=donations)

# --- General Profile Page ---
@app.route('/profile')
def profile():
    if 'user' not in session: return redirect(url_for('login'))
    user_data = query_db("SELECT username, role, created_at FROM User WHERE username = %s", [session.get('user')], one=True)
    return render_template('profile.html', user=user_data)


# --- Main Execution ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
