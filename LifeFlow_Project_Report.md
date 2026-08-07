# LifeFlow - Blood Donation Management System
## Project Report

---

## 1. Introduction

LifeFlow is a comprehensive Blood Donation Management System designed to streamline and automate the process of blood donation, storage, and distribution. The system provides a centralized platform for managing donors, recipients, blood banks, and blood stock inventory.

The application leverages modern web technologies to create an efficient, user-friendly interface for both administrative staff and regular users (donors). It enables blood banks to maintain accurate records of donations, track blood inventory, manage recipient requests, and generate detailed reports for analysis and decision-making.

**Key Stakeholders:**
- **Administrators/Staff**: Manage the entire system, including donors, recipients, blood stock, and generate reports
- **Donors**: Register as donors, update their profiles, view donation history, and request blood when needed
- **Recipients**: Request blood based on medical needs

---

## 2. Problem Statement

Blood donation and management systems face several critical challenges:

1. **Lack of Centralized Database**: Many blood banks operate in isolation, making it difficult to track available blood units across multiple locations.

2. **Manual Record Keeping**: Traditional paper-based systems are prone to errors, data loss, and inefficiency in managing donor and recipient information.

3. **Inventory Management**: Tracking blood stock, expiry dates, and maintaining optimal inventory levels is challenging without automated systems.

4. **Donor Engagement**: Difficulty in maintaining donor records, tracking donation history, and ensuring donor eligibility for future donations.

5. **Emergency Response**: During medical emergencies, quick access to blood type availability and donor information is critical but often delayed.

6. **Reporting and Analytics**: Generating insights on donation patterns, blood type demand, and inventory trends requires significant manual effort.

**LifeFlow Solution:**
LifeFlow addresses these challenges by providing a web-based, database-driven solution that centralizes blood donation management, automates record-keeping, provides real-time inventory tracking, and generates comprehensive reports for data-driven decision-making.

---

## 3. System Architecture and Modules

### System Architecture

LifeFlow follows a **Three-Tier Architecture**:

```
┌─────────────────────────────────────┐
│     Presentation Layer (Frontend)   │
│   - HTML Templates (Jinja2)         │
│   - JavaScript (Charts, Validation) │
│   - CSS Styling                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Application Layer (Backend)     │
│   - Flask Web Framework             │
│   - Session Management              │
│   - Authentication & Authorization  │
│   - Business Logic                  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Data Layer (Database)         │
│   - MySQL Database                  │
│   - Tables, Views, Procedures       │
│   - Data Storage & Retrieval        │
└─────────────────────────────────────┘
```

### Technology Stack

- **Backend Framework**: Flask (Python) v2.0+
- **Database**: MySQL v8.0+
- **Authentication**: Werkzeug password hashing, Flask sessions
- **Frontend**: HTML5, CSS3, JavaScript
- **Charting**: JavaScript charting libraries
- **Environment Management**: python-dotenv
- **Template Engine**: Jinja2

### Core Modules

#### 3.1 Authentication Module
- User registration with role-based access (Admin, Staff, User)
- Secure login with password hashing
- Session management with timeout
- Role-based access control

#### 3.2 Donor Management Module
- Donor registration with comprehensive details
- Profile editing and updates
- Eligibility status tracking
- Donation history maintenance

#### 3.3 Recipient Management Module
- Recipient registration
- Medical notes and requirements tracking
- Blood request processing

#### 3.4 Blood Stock Management Module
- Blood unit tracking by blood group
- Expiry date monitoring
- Storage location management
- Bank-wise inventory tracking

#### 3.5 Donation Processing Module
- Recording new donations
- Linking donors to blood units
- Donation date and quantity tracking

#### 3.6 Blood Issue Module
- Blood distribution to recipients
- Hospital and issue date tracking
- Quantity management

#### 3.7 Reporting Module
- Monthly donation reports
- Yearly donation summaries
- Blood stock summaries
- Dashboard analytics

#### 3.8 User Dashboard Module
- Donor profile management
- Personal donation history
- Blood request submission

---

## 4. Functional Requirements

### 4.1 User Management
- **FR-1.1**: System shall allow new users to register with username, password, and role
- **FR-1.2**: System shall authenticate users with encrypted passwords
- **FR-1.3**: System shall maintain session state for logged-in users
- **FR-1.4**: System shall provide role-based access (Admin, Staff, User)
- **FR-1.5**: System shall allow users to logout and clear session data

### 4.2 Donor Management
- **FR-2.1**: System shall allow registration of donors with personal and medical details
- **FR-2.2**: System shall validate donor email uniqueness
- **FR-2.3**: System shall track last donation date and eligibility status
- **FR-2.4**: System shall allow donors to update their profile information
- **FR-2.5**: System shall display list of all donors to admin/staff
- **FR-2.6**: System shall link donor accounts to user accounts

### 4.3 Recipient Management
- **FR-3.1**: System shall register recipients with required blood group information
- **FR-3.2**: System shall store medical notes and registration dates
- **FR-3.3**: System shall display recipient list to authorized users

### 4.4 Blood Stock Management
- **FR-4.1**: System shall track blood units by blood group
- **FR-4.2**: System shall monitor collection and expiry dates
- **FR-4.3**: System shall assign storage locations to blood units
- **FR-4.4**: System shall associate blood units with blood banks
- **FR-4.5**: System shall provide blood stock summary by blood group

### 4.5 Donation Processing
- **FR-5.1**: System shall record donation transactions
- **FR-5.2**: System shall link donations to donors and blood units
- **FR-5.3**: System shall track donation dates and quantities
- **FR-5.4**: System shall update donor's last donation date

### 4.6 Blood Distribution
- **FR-6.1**: System shall record blood issues to recipients
- **FR-6.2**: System shall track hospital and issue date
- **FR-6.3**: System shall manage blood unit quantities

### 4.7 Reporting
- **FR-7.1**: System shall generate monthly donation reports
- **FR-7.2**: System shall generate yearly donation summaries
- **FR-7.3**: System shall provide downloadable report files
- **FR-7.4**: System shall display dashboard statistics
- **FR-7.5**: System shall visualize blood stock data

### 4.8 User Features
- **FR-8.1**: System shall allow users to view their donation history
- **FR-8.2**: System shall provide user profile management
- **FR-8.3**: System shall enable blood request submission
- **FR-8.4**: System shall validate user input on forms

---

## 5. Entities, Relationships, and Attributes

### Entity-Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  Blood_Bank │───────│ Blood_Stock │───────│  Donation   │
└─────────────┘   1:N └─────────────┘  1:N  └─────────────┘
                              │                      │
                              │ 1:N                  │ N:1
                              │                      │
                        ┌─────▼────────┐      ┌─────▼────┐
                        │ Blood_Issue  │      │  Donor   │
                        └──────────────┘      └──────────┘
                              │                      │
                              │ N:1                  │ 1:1
                              │                      │
                        ┌─────▼────────┐      ┌─────▼────┐
                        │  Recipient   │      │   User   │
                        └──────────────┘      └──────────┘
```

### Entity Descriptions

#### 5.1 Blood_Bank
**Description**: Represents blood bank facilities where blood is stored

**Attributes**:
- `bank_id` (INT, PK, AUTO_INCREMENT): Unique identifier for blood bank
- `name` (VARCHAR(100)): Name of the blood bank
- `address` (VARCHAR(200)): Physical address
- `contact` (VARCHAR(100)): Contact information

#### 5.2 Donor
**Description**: Stores information about blood donors

**Attributes**:
- `donor_id` (INT, PK, AUTO_INCREMENT): Unique donor identifier
- `name` (VARCHAR(100)): Donor's full name
- `age` (INT): Age of donor (18-65)
- `gender` (CHAR(1)): Gender (M/F/O)
- `blood_group` (VARCHAR(5)): Blood type (A+, A-, B+, B-, AB+, AB-, O+, O-)
- `contact` (VARCHAR(20)): Phone number
- `address` (VARCHAR(255)): Residential address
- `email` (VARCHAR(100), UNIQUE): Email address
- `last_donation_date` (DATE): Date of last donation
- `eligibility_status` (VARCHAR(30)): Current eligibility status

#### 5.3 Recipient
**Description**: Contains recipient information and blood requirements

**Attributes**:
- `recipient_id` (INT, PK, AUTO_INCREMENT): Unique recipient identifier
- `name` (VARCHAR(100)): Recipient's name
- `age` (INT): Age
- `gender` (CHAR(1)): Gender
- `blood_group_needed` (VARCHAR(5)): Required blood type
- `contact` (VARCHAR(20)): Contact number
- `address` (VARCHAR(255)): Address
- `medical_notes` (VARCHAR(255)): Medical condition notes
- `registration_date` (DATE): Registration date

#### 5.4 Blood_Stock
**Description**: Tracks blood inventory units

**Attributes**:
- `unit_id` (INT, PK, AUTO_INCREMENT): Unique blood unit identifier
- `blood_group` (VARCHAR(5)): Blood type
- `quantity` (INT): Number of units
- `collection_date` (DATE): Date blood was collected
- `expiry_date` (DATE): Expiration date
- `storage_location` (VARCHAR(50)): Storage facility location
- `bank_id` (INT, FK → Blood_Bank): Associated blood bank

#### 5.5 Donation
**Description**: Records donation transactions

**Attributes**:
- `donation_id` (INT, PK, AUTO_INCREMENT): Unique donation identifier
- `donor_id` (INT, FK → Donor): Donor who made donation
- `unit_id` (INT, FK → Blood_Stock): Blood unit created
- `donation_date` (DATE): Date of donation
- `quantity` (INT): Quantity donated

#### 5.6 Blood_Issue
**Description**: Tracks blood distribution to recipients

**Attributes**:
- `issue_id` (INT, PK, AUTO_INCREMENT): Unique issue identifier
- `recipient_id` (INT, FK → Recipient): Recipient receiving blood
- `unit_id` (INT, FK → Blood_Stock): Blood unit issued
- `issue_date` (DATE): Date of issue
- `hospital` (VARCHAR(100)): Hospital name
- `quantity` (INT): Quantity issued

#### 5.7 User
**Description**: System users with authentication credentials

**Attributes**:
- `user_id` (INT, PK, AUTO_INCREMENT): Unique user identifier
- `username` (VARCHAR(50), UNIQUE): Login username
- `password_hash` (VARCHAR(255)): Encrypted password
- `role` (ENUM): User role (admin/staff/user)
- `created_at` (DATE): Account creation date
- `donor_id` (INT, FK → Donor, NULLABLE): Linked donor profile

#### 5.8 Monthly_Donation_Report
**Description**: Aggregated monthly donation statistics

**Attributes**:
- `report_id` (INT, PK, AUTO_INCREMENT): Report identifier
- `year` (INT): Year
- `month` (INT): Month
- `total_donations` (INT): Total donations count
- `total_quantity` (INT): Total units donated
- `created_at` (TIMESTAMP): Report generation timestamp

#### 5.9 Yearly_Donation_Report
**Description**: Aggregated yearly donation statistics

**Attributes**:
- `report_id` (INT, PK, AUTO_INCREMENT): Report identifier
- `year` (INT, UNIQUE): Year
- `total_donations` (INT): Total donations count
- `total_quantity` (INT): Total units donated
- `created_at` (TIMESTAMP): Report generation timestamp

### Relationships

1. **Blood_Bank → Blood_Stock**: One-to-Many
   - One blood bank can store multiple blood units

2. **Donor → Donation**: One-to-Many
   - One donor can make multiple donations over time

3. **Blood_Stock → Donation**: One-to-Many
   - One blood unit can be associated with multiple donation records

4. **Blood_Stock → Blood_Issue**: One-to-Many
   - One blood stock entry can have multiple issues

5. **Recipient → Blood_Issue**: One-to-Many
   - One recipient can receive blood multiple times

6. **User → Donor**: One-to-One (Optional)
   - A user account can be linked to one donor profile

---

## 6. Relational Schema

### Normalized Database Schema

```sql
Blood_Bank (
    bank_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    address VARCHAR(200),
    contact VARCHAR(100)
)

Donor (
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

Recipient (
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

Blood_Stock (
    unit_id INT PRIMARY KEY AUTO_INCREMENT,
    blood_group VARCHAR(5),
    quantity INT,
    collection_date DATE,
    expiry_date DATE,
    storage_location VARCHAR(50),
    bank_id INT,
    FOREIGN KEY (bank_id) REFERENCES Blood_Bank(bank_id)
)

Donation (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    donor_id INT,
    unit_id INT,
    donation_date DATE,
    quantity INT,
    FOREIGN KEY (donor_id) REFERENCES Donor(donor_id),
    FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id)
)

Blood_Issue (
    issue_id INT PRIMARY KEY AUTO_INCREMENT,
    recipient_id INT,
    unit_id INT,
    issue_date DATE,
    hospital VARCHAR(100),
    quantity INT,
    FOREIGN KEY (recipient_id) REFERENCES Recipient(recipient_id),
    FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id)
)

User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('admin', 'staff', 'user'),
    created_at DATE,
    donor_id INT,
    FOREIGN KEY (donor_id) REFERENCES Donor(donor_id)
)

Monthly_Donation_Report (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    month INT,
    total_donations INT,
    total_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY year_month_unique (year, month)
)

Yearly_Donation_Report (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT UNIQUE,
    total_donations INT,
    total_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Normalization Analysis

**Third Normal Form (3NF) Compliance:**

All tables in LifeFlow database are in Third Normal Form:

1. **First Normal Form (1NF)**:
   - All attributes contain atomic values
   - No repeating groups
   - Each table has a primary key

2. **Second Normal Form (2NF)**:
   - All non-key attributes are fully functionally dependent on primary key
   - No partial dependencies

3. **Third Normal Form (3NF)**:
   - No transitive dependencies
   - All non-key attributes depend only on primary key

---

## 7. Implementation

### a) Database Setup

#### Installation Steps

**Step 1: Install MySQL Server**

1. Download MySQL Community Server (v8.0+) from official website
2. Run the installer and follow the setup wizard
3. Configure MySQL Server:
   - Select "Development Machine" configuration
   - Set root password
   - Configure MySQL as Windows Service
   - Create user account for application

**Step 2: Create Database User**

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create application user
CREATE USER 'Nirrmam'@'localhost' IDENTIFIED BY 'lifeflow';

-- Grant privileges
GRANT ALL PRIVILEGES ON blood_donation.* TO 'Nirrmam'@'localhost';
FLUSH PRIVILEGES;
```

**Step 3: Configure Environment Variables**

Create a `.env` file in project root:

```
DB_HOST=localhost
DB_USER=Nirrmam
DB_PASSWORD=lifeflow
DB_NAME=blood_donation
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-super-secret-jwt-key
```

**Step 4: Install Python Dependencies**

```bash
# Navigate to project directory
cd Lifeflow

# Install requirements
pip install -r requirements.txt
```

**Step 5: Execute Database Schema**

```bash
# Connect to MySQL
mysql -u Nirrmam -p

# Execute schema file
source database/schema.sql
```

---

### b) Table Creation Scripts

#### Complete Database Schema

```sql
-- Drop the database if it exists to start fresh
DROP DATABASE IF EXISTS blood_donation;

-- Create and use the new database
CREATE DATABASE blood_donation;
USE blood_donation;

-- Blood_Bank table
CREATE TABLE Blood_Bank (
    bank_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    address VARCHAR(200),
    contact VARCHAR(100)
);

-- Donor table
CREATE TABLE Donor (
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
);

-- Recipient table
CREATE TABLE Recipient (
    recipient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    gender CHAR(1),
    blood_group_needed VARCHAR(5),
    contact VARCHAR(20),
    address VARCHAR(255),
    medical_notes VARCHAR(255),
    registration_date DATE
);

-- Blood_Stock table
CREATE TABLE Blood_Stock (
    unit_id INT PRIMARY KEY AUTO_INCREMENT,
    blood_group VARCHAR(5),
    quantity INT,
    collection_date DATE,
    expiry_date DATE,
    storage_location VARCHAR(50),
    bank_id INT,
    FOREIGN KEY (bank_id) REFERENCES Blood_Bank(bank_id)
);

-- Donation table
CREATE TABLE Donation (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    donor_id INT,
    unit_id INT,
    donation_date DATE,
    quantity INT,
    FOREIGN KEY (donor_id) REFERENCES Donor(donor_id),
    FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id)
);

-- Blood_Issue table
CREATE TABLE Blood_Issue (
    issue_id INT PRIMARY KEY AUTO_INCREMENT,
    recipient_id INT,
    unit_id INT,
    issue_date DATE,
    hospital VARCHAR(100),
    quantity INT,
    FOREIGN KEY (recipient_id) REFERENCES Recipient(recipient_id),
    FOREIGN KEY (unit_id) REFERENCES Blood_Stock(unit_id)
);

-- User table
CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    role ENUM('admin', 'staff', 'user'),
    created_at DATE,
    donor_id INT,
    FOREIGN KEY (donor_id) REFERENCES Donor(donor_id)
);

-- Monthly Donation Report table
CREATE TABLE Monthly_Donation_Report (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    month INT,
    total_donations INT,
    total_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY year_month_unique (year, month)
);

-- Yearly Donation Report table
CREATE TABLE Yearly_Donation_Report (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT UNIQUE,
    total_donations INT,
    total_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### c) Stored Procedures, Views, and Indexes

#### Views

**Blood_Stock_Summary View**

Purpose: Provides aggregated view of blood stock by blood group

```sql
CREATE VIEW Blood_Stock_Summary AS
SELECT 
    blood_group,
    SUM(quantity) as total_units
FROM Blood_Stock
GROUP BY blood_group;
```

Usage:
```sql
-- Get summary of all blood groups
SELECT * FROM Blood_Stock_Summary;

-- Check specific blood group availability
SELECT total_units FROM Blood_Stock_Summary WHERE blood_group = 'O+';
```

#### Stored Procedures

**1. generate_monthly_report**

Purpose: Generates monthly donation statistics and stores them in Monthly_Donation_Report table

```sql
DELIMITER //
CREATE PROCEDURE generate_monthly_report(IN p_year INT, IN p_month INT)
BEGIN
    INSERT INTO Monthly_Donation_Report (year, month, total_donations, total_quantity)
    SELECT 
        YEAR(donation_date) as year,
        MONTH(donation_date) as month,
        COUNT(*) as total_donations,
        SUM(quantity) as total_quantity
    FROM Donation
    WHERE YEAR(donation_date) = p_year AND MONTH(donation_date) = p_month
    GROUP BY YEAR(donation_date), MONTH(donation_date)
    ON DUPLICATE KEY UPDATE
        total_donations = VALUES(total_donations),
        total_quantity = VALUES(total_quantity);
END //
DELIMITER ;
```

Usage:
```sql
-- Generate report for September 2025
CALL generate_monthly_report(2025, 9);
```

**2. generate_yearly_report**

Purpose: Generates yearly donation statistics and stores them in Yearly_Donation_Report table

```sql
DELIMITER //
CREATE PROCEDURE generate_yearly_report(IN p_year INT)
BEGIN
    INSERT INTO Yearly_Donation_Report (year, total_donations, total_quantity)
    SELECT 
        YEAR(donation_date) as year,
        COUNT(*) as total_donations,
        SUM(quantity) as total_quantity
    FROM Donation
    WHERE YEAR(donation_date) = p_year
    GROUP BY YEAR(donation_date)
    ON DUPLICATE KEY UPDATE
        total_donations = VALUES(total_donations),
        total_quantity = VALUES(total_quantity);
END //
DELIMITER ;
```

Usage:
```sql
-- Generate report for year 2025
CALL generate_yearly_report(2025);
```

#### Indexes

**Implicit Indexes:**
- Primary keys automatically create clustered indexes
- Unique constraints create unique indexes

**Recommended Additional Indexes:**

```sql
-- Index on donor email for faster lookup
CREATE INDEX idx_donor_email ON Donor(email);

-- Index on donor blood group for filtering
CREATE INDEX idx_donor_blood_group ON Donor(blood_group);

-- Index on blood stock expiry date for monitoring
CREATE INDEX idx_stock_expiry ON Blood_Stock(expiry_date);

-- Index on donation date for reporting
CREATE INDEX idx_donation_date ON Donation(donation_date);

-- Index on username for authentication
CREATE INDEX idx_user_username ON User(username);
```

---

### d) Sample Data

#### Blood Banks (3 entries)

```sql
INSERT INTO Blood_Bank (name, address, contact) VALUES
('Central Blood Bank', '123 Main St, City', '123-456-7890'),
('Westside Blood Bank', '456 West St, City', '987-654-3210'),
('Eastside Blood Center', '789 East Blvd, City', '321-654-0987');
```

#### Donors (15 entries)

| ID | Name | Age | Gender | Blood Group | Contact | Email | Last Donation | Status |
|----|------|-----|--------|-------------|---------|-------|---------------|--------|
| 1 | John Doe | 30 | M | A+ | 555-1234 | john.doe@example.com | 2025-07-01 | Eligible |
| 2 | Jane Smith | 28 | F | O- | 555-5678 | jane.smith@example.com | 2025-06-15 | Eligible |
| 3 | Mike Johnson | 42 | M | B+ | 555-2468 | mike.j@example.com | 2025-05-30 | Eligible |
| 4 | Emily Davis | 35 | F | AB+ | 555-1357 | emily.d@example.com | 2025-04-20 | Eligible |
| 5 | Chris Lee | 50 | M | O+ | 555-9753 | chris.lee@example.com | 2025-03-10 | Eligible |
| 6 | Sarah Wilson | 25 | F | A- | 555-8642 | sarah.w@example.com | 2025-08-11 | Eligible |
| 7 | David Brown | 33 | M | B- | 555-7531 | david.b@example.com | 2025-07-22 | Eligible |
| 8 | Linda White | 41 | F | AB- | 555-9876 | linda.w@example.com | 2025-09-01 | Eligible |
| 9 | James Green | 29 | M | O+ | 555-2345 | james.g@example.com | 2025-06-25 | Eligible |
| 10 | Patricia Harris | 38 | F | A+ | 555-6789 | patricia.h@example.com | 2025-08-18 | Eligible |

#### Recipients (15 entries)

| ID | Name | Age | Gender | Blood Needed | Contact | Medical Notes | Registration |
|----|------|-----|--------|--------------|---------|---------------|--------------|
| 1 | Michael Johnson | 45 | M | A+ | 555-8765 | Urgent transfusion required | 2025-08-20 |
| 2 | Susan Williams | 50 | F | O- | 555-4321 | Post-surgery recovery | 2025-08-22 |
| 3 | Paul Lewis | 55 | M | B+ | 555-6780 | Scheduled heart surgery | 2025-08-15 |
| 4 | Nancy King | 60 | F | AB+ | 555-7891 | Anemia treatment | 2025-09-02 |
| 5 | Kevin Young | 47 | M | O+ | 555-8902 | Cancer therapy support | 2025-08-28 |

#### Blood Stock (15 entries)

| Unit ID | Blood Group | Quantity | Collection Date | Expiry Date | Storage | Bank ID |
|---------|-------------|----------|-----------------|-------------|---------|---------|
| 1 | A+ | 25 | 2025-09-10 | 2025-10-22 | Fridge A1 | 1 |
| 2 | O- | 15 | 2025-09-08 | 2025-10-20 | Fridge A2 | 1 |
| 3 | B+ | 20 | 2025-09-11 | 2025-10-23 | Fridge B1 | 2 |
| 4 | AB+ | 10 | 2025-09-09 | 2025-10-21 | Fridge B2 | 2 |
| 5 | O+ | 35 | 2025-09-12 | 2025-10-24 | Fridge C1 | 3 |

**Blood Stock Summary by Group:**

| Blood Group | Total Units |
|-------------|-------------|
| A+ | 47 |
| O- | 29 |
| B+ | 48 |
| AB+ | 21 |
| O+ | 75 |
| A- | 28 |
| B- | 28 |
| AB- | 8 |

#### Donations (15 entries)

Sample donation records linking donors to blood units:

```sql
INSERT INTO Donation (donor_id, unit_id, donation_date, quantity) VALUES
(1, 1, '2025-09-10', 1),
(2, 2, '2025-09-08', 1),
(3, 3, '2025-09-11', 1),
-- ... (12 more entries)
```

---

## 8. User Interface

### a) Screenshots of the UI

Below are descriptions of key user interface screens in the LifeFlow system:

#### 1. Login Page
**File**: `templates/login.html`
**Description**: User authentication screen with username and password fields
**Features**:
- Clean, professional login form
- Username input field
- Password input field (masked)
- Login button
- Link to registration page
- Flash message display for errors/success
- Responsive design

#### 2. Registration Page
**File**: `templates/register.html`
**Description**: New user registration interface
**Features**:
- Username input (validated for uniqueness)
- Password input with confirmation
- Role selection (Admin/Staff/User)
- Registration button
- Link back to login page
- Client-side validation

#### 3. Admin Dashboard
**File**: `templates/dashboard.html`
**Description**: Main administrative control panel
**Features**:
- Statistics cards showing:
  - Total Donors
  - Total Recipients
  - Blood Units Available
- Quick navigation menu
- Blood stock visualization charts
- Recent activity summary
- Links to all management modules

#### 4. Donor Management Page
**File**: `templates/donors.html`
**Description**: Comprehensive donor listing and management
**Features**:
- Tabular display of all donors
- Columns: Name, Age, Gender, Blood Group, Contact, Email, Last Donation, Status
- Edit button for each donor
- Add new donor button
- Search/filter functionality
- Pagination for large datasets
- Responsive table design

#### 5. Add Donor Page
**File**: `templates/add_donor.html`
**Description**: Form for registering new donors
**Features**:
- Input fields:
  - Full Name
  - Age (18-65 validation)
  - Gender (dropdown)
  - Blood Group (dropdown: A+, A-, B+, B-, AB+, AB-, O+, O-)
  - Contact Number
  - Email (unique validation)
  - Address
  - Last Donation Date (optional)
  - Eligibility Status
- Client-side validation (JavaScript)
- Server-side validation
- Submit and Cancel buttons
- Clear error messaging

#### 6. Edit Donor Page
**File**: `templates/edit_donor.html`
**Description**: Form for updating existing donor information
**Features**:
- Pre-populated form fields with current donor data
- Same validation as add donor form
- Update button
- Cancel button (redirects to donor list)
- Success/error flash messages

#### 7. Recipients Page
**File**: `templates/recipients.html`
**Description**: Recipient management interface
**Features**:
- Table of recipients with columns:
  - Name
  - Age
  - Gender
  - Blood Group Needed
  - Contact
  - Medical Notes
  - Registration Date
- Add recipient functionality
- Filter by blood group needed
- View medical notes

#### 8. Blood Stock Page
**File**: `templates/stock.html`
**Description**: Blood inventory management
**Features**:
- Stock table showing:
  - Blood Group
  - Quantity
  - Collection Date
  - Expiry Date
  - Storage Location
  - Bank Name
- Color coding for expiring units
- Total units by blood group
- Add new stock functionality
- Visual indicators for low stock

#### 9. Reports Page
**File**: `templates/reports.html`
**Description**: Report generation and viewing interface
**Features**:
- Monthly reports section:
  - Year/Month selector
  - Generate button
  - Download as text file
- Yearly reports section:
  - Year selector
  - Generate button
  - Download functionality
- Historical reports table
- Blood stock summary charts
- Export options

#### 10. User Dashboard
**File**: `templates/user_dashboard.html`
**Description**: Donor-specific dashboard
**Features**:
- Welcome message
- Quick stats:
  - Number of donations made
  - Last donation date
  - Eligibility status
- Quick action buttons:
  - View/Edit Profile
  - View Donation History
  - Request Blood
- Upcoming donation eligibility date
- Blood bank contact information

#### 11. User Profile Page
**File**: `templates/user_profile.html`
**Description**: Personal donor profile management
**Features**:
- Display mode:
  - All donor information displayed
  - Edit button
- Edit mode:
  - Editable form fields
  - Save changes button
  - Cancel button
- Profile validation (JavaScript file: `profile-validation.js`)
- Real-time field validation
- Success/error messaging

#### 12. Donation History Page
**File**: `templates/user_donations.html`
**Description**: Personal donation records for donors
**Features**:
- Table of past donations:
  - Donation Date
  - Blood Bank Name
  - Quantity Donated
- Sorted by date (most recent first)
- Total donations count
- Total quantity donated
- Empty state message if no donations

#### 13. Blood Request Page
**File**: `templates/request_blood.html`
**Description**: Form for requesting blood
**Features**:
- Blood group selector
- Units needed input
- Hospital name
- Urgency level (dropdown)
- Contact information
- Additional notes field
- Submit request button
- Request status tracking

#### 14. Layout Template
**File**: `templates/layout.html`
**Description**: Base template for consistent UI across all pages
**Features**:
- Navigation bar with role-based menu items
- Flash message container
- Footer with system information
- Responsive design framework
- CSS and JavaScript includes
- Session-based user greeting

### UI Design Principles

1. **Consistency**: All pages use the common layout template ensuring uniform navigation and styling

2. **Responsive Design**: Mobile-friendly interfaces that adapt to different screen sizes

3. **User Feedback**: Flash messages for all user actions (success, error, warning)

4. **Accessibility**: Clear labels, proper form structure, keyboard navigation support

5. **Validation**: Client-side (JavaScript) and server-side validation for data integrity

6. **Role-Based Access**: UI elements shown/hidden based on user role

7. **Data Visualization**: Charts and graphs for dashboard analytics using `dashboard_charts.js`

### JavaScript Components

**dashboard_charts.js**: Visualization library integration for:
- Blood stock pie/bar charts
- Donation trends over time
- Real-time dashboard updates via AJAX

**profile-validation.js**: Form validation for:
- Email format validation
- Phone number format
- Age range checking
- Required field validation
- Real-time feedback

---

## 9. Conclusion

LifeFlow successfully implements a comprehensive Blood Donation Management System that addresses critical challenges in blood bank operations. The system provides:

### Key Achievements

1. **Centralized Data Management**: Single source of truth for all donor, recipient, and inventory data
2. **Automated Workflows**: Streamlined donation processing and blood issue tracking
3. **Real-time Inventory**: Up-to-date blood stock information with expiry monitoring
4. **Comprehensive Reporting**: Automated monthly and yearly reports for decision-making
5. **User Empowerment**: Donors can manage their profiles and view donation history
6. **Security**: Role-based access control and secure password handling

### Technical Highlights

- **Database Design**: Normalized schema (3NF) ensuring data integrity
- **Stored Procedures**: Efficient report generation and data aggregation
- **Views**: Simplified queries for blood stock summaries
- **Web Framework**: Flask-based backend with session management
- **Frontend**: Responsive HTML templates with JavaScript validation

### Future Enhancements

1. **SMS/Email Notifications**: Alert donors when eligible to donate again
2. **Mobile Application**: Native mobile apps for donors and staff
3. **Geo-location**: Find nearest blood banks with required blood type
4. **Appointment Scheduling**: Online booking for donation appointments
5. **Advanced Analytics**: Predictive analytics for blood demand forecasting
6. **Integration**: Connect with hospital systems for real-time requests
7. **QR Code**: Generate QR codes for donors for quick check-in

### System Impact

LifeFlow demonstrates how modern web technologies and database management can revolutionize traditional blood donation processes, making them more efficient, transparent, and accessible to all stakeholders.

---

## 10. References

1. Flask Documentation: https://flask.palletsprojects.com/
2. MySQL Documentation: https://dev.mysql.com/doc/
3. Werkzeug Security: https://werkzeug.palletsprojects.com/
4. Bootstrap Framework: https://getbootstrap.com/
5. Python dotenv: https://pypi.org/project/python-dotenv/

---

## Appendix

### A. Installation Commands

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start MySQL service (Windows)
net start MySQL80

# Run database schema
mysql -u Nirrmam -p < database/schema.sql

# Start Flask application
python backend/app.py
```

### B. Environment Configuration Template

```
DB_HOST=localhost
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=blood_donation
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
```

### C. Project Structure

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
│   ├── register.html
│   ├── dashboard.html
│   ├── donors.html
│   ├── add_donor.html
│   ├── edit_donor.html
│   ├── recipients.html
│   ├── stock.html
│   ├── reports.html
│   ├── user_dashboard.html
│   ├── user_profile.html
│   ├── user_donations.html
│   └── request_blood.html
├── .env
├── requirements.txt
└── README.md
```

---

**Document Prepared By**: LifeFlow Development Team  
**Date**: November 2025  
**Version**: 1.0  
**Status**: Final
