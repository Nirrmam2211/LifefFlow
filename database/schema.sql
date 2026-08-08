-- Drop the database if it exists to start fresh
DROP DATABASE IF EXISTS blood_donation;

-- Create and use the new database
CREATE DATABASE blood_donation;
USE blood_donation;

-- Table Creation --

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

-- Blood_Request table
CREATE TABLE Blood_Request (
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
);

-- Create tables for monthly and yearly reports
USE blood_donation;

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

-- Create view for Blood Stock Summary
CREATE VIEW Blood_Stock_Summary AS
SELECT 
    blood_group,
    SUM(quantity) as total_units
FROM Blood_Stock
GROUP BY blood_group;

-- Create stored procedure to generate monthly report
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

-- Create stored procedure to generate yearly report
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

-- Function to check donor eligibility based on last donation date (e.g., 90 days interval)
DELIMITER //
CREATE FUNCTION check_donor_eligibility(p_last_donation_date DATE)
RETURNS VARCHAR(30)
DETERMINISTIC
BEGIN
    DECLARE days_since_last_donation INT;
    IF p_last_donation_date IS NULL THEN
        RETURN 'Eligible';
    END IF;
    SET days_since_last_donation = DATEDIFF(CURDATE(), p_last_donation_date);
    IF days_since_last_donation >= 90 THEN
        RETURN 'Eligible';
    ELSE
        RETURN 'Not Eligible';
    END IF;
END //
DELIMITER ;

-- Function to get total blood quantity for a specific blood group
DELIMITER //
CREATE FUNCTION get_blood_stock_quantity(p_blood_group VARCHAR(5))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_quantity INT;
    SELECT SUM(quantity) INTO total_quantity
    FROM Blood_Stock
    WHERE blood_group = p_blood_group;
    RETURN IFNULL(total_quantity, 0);
END //
DELIMITER ;

-- Function to get the number of eligible donors for a specific blood group
DELIMITER //
CREATE FUNCTION get_eligible_donors_count(p_blood_group VARCHAR(5))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE eligible_count INT;
    SELECT COUNT(*) INTO eligible_count
    FROM Donor
    WHERE blood_group = p_blood_group AND eligibility_status = 'Eligible';
    RETURN IFNULL(eligible_count, 0);
END //
DELIMITER ;

-- Sample Data Insertion --

-- Blood_Bank data
INSERT INTO Blood_Bank (name, address, contact) VALUES
('Central Blood Bank', '123 Main St, City', '123-456-7890'),
('Westside Blood Bank', '456 West St, City', '987-654-3210'),
('Eastside Blood Center', '789 East Blvd, City', '321-654-0987');

-- Donor data (15 entries)
INSERT INTO Donor (name, age, gender, blood_group, contact, address, email, last_donation_date, eligibility_status) VALUES
('John Doe', 30, 'M', 'A+', '555-1234', '12 Elm St', 'john.doe@example.com', '2025-07-01', 'Eligible'),
('Jane Smith', 28, 'F', 'O-', '555-5678', '34 Pine St', 'jane.smith@example.com', '2025-06-15', 'Eligible'),
('Mike Johnson', 42, 'M', 'B+', '555-2468', '56 Maple St', 'mike.j@example.com', '2025-05-30', 'Eligible'),
('Emily Davis', 35, 'F', 'AB+', '555-1357', '78 Oak St', 'emily.d@example.com', '2025-04-20', 'Eligible'),
('Chris Lee', 50, 'M', 'O+', '555-9753', '90 Birch St', 'chris.lee@example.com', '2025-03-10', 'Eligible'),
('Sarah Wilson', 25, 'F', 'A-', '555-8642', '101 Cedar St', 'sarah.w@example.com', '2025-08-11', 'Eligible'),
('David Brown', 33, 'M', 'B-', '555-7531', '112 Spruce St', 'david.b@example.com', '2025-07-22', 'Eligible'),
('Linda White', 41, 'F', 'AB-', '555-9876', '123 Walnut St', 'linda.w@example.com', '2025-09-01', 'Eligible'),
('James Green', 29, 'M', 'O+', '555-2345', '134 Chestnut St', 'james.g@example.com', '2025-06-25', 'Eligible'),
('Patricia Harris', 38, 'F', 'A+', '555-6789', '145 Fir St', 'patricia.h@example.com', '2025-08-18', 'Eligible'),
('Robert Clark', 45, 'M', 'B+', '555-3456', '156 Pine St', 'robert.c@example.com', '2025-09-05', 'Eligible'),
('Jessica Lewis', 22, 'F', 'O-', '555-4567', '167 Oak St', 'jessica.l@example.com', '2025-07-30', 'Eligible'),
('Daniel Walker', 31, 'M', 'AB+', '555-7890', '178 Maple St', 'daniel.w@example.com', '2025-08-21', 'Eligible'),
('Laura Hall', 27, 'F', 'A-', '555-5432', '189 Birch St', 'laura.h@example.com', '2025-09-10', 'Eligible'),
('Kevin Allen', 39, 'M', 'B-', '555-2109', '200 Cedar St', 'kevin.a@example.com', '2025-08-05', 'Eligible');

-- Recipient data (15 entries)
INSERT INTO Recipient (name, age, gender, blood_group_needed, contact, address, medical_notes, registration_date) VALUES
('Michael Johnson', 45, 'M', 'A+', '555-8765', '210 Oak St', 'Urgent transfusion required', '2025-08-20'),
('Susan Williams', 50, 'F', 'O-', '555-4321', '221 Maple St', 'Post-surgery recovery', '2025-08-22'),
('Paul Lewis', 55, 'M', 'B+', '555-6780', '232 Elm St', 'Scheduled heart surgery', '2025-08-15'),
('Nancy King', 60, 'F', 'AB+', '555-7891', '243 Pine St', 'Anemia treatment', '2025-09-02'),
('Kevin Young', 47, 'M', 'O+', '555-8902', '254 Fir St', 'Cancer therapy support', '2025-08-28'),
('Jennifer Wright', 44, 'F', 'A-', '555-9012', '265 Spruce St', 'Accident victim', '2025-09-11'),
('Brian Scott', 56, 'M', 'B-', '555-0123', '276 Cedar St', 'Critically ill', '2025-09-08'),
('Linda Adams', 42, 'F', 'AB-', '555-1230', '287 Walnut St', 'Immune disorder', '2025-08-25'),
('George Baker', 65, 'M', 'O+', '555-2341', '298 Chestnut St', 'Emergency case', '2025-09-14'),
('Karen Nelson', 53, 'F', 'A+', '555-3452', '309 Oak St', 'Pre-operative needs', '2025-09-03'),
('Charles Carter', 49, 'M', 'B+', '555-4563', '320 Maple St', 'Chronic blood disorder', '2025-08-30'),
('Barbara Mitchell', 37, 'F', 'O-', '555-5674', '331 Birch St', 'Maternity complications', '2025-09-07'),
('Daniel Perez', 46, 'M', 'AB+', '555-6785', '342 Cedar St', 'Organ transplant recipient', '2025-09-12'),
('Betty Roberts', 38, 'F', 'A-', '555-7896', '353 Spruce St', 'Leukemia treatment', '2025-08-29'),
('Matthew Turner', 59, 'M', 'B-', '555-8907', '364 Walnut St', 'Kidney dialysis support', '2025-09-06');

-- Blood_Stock data (15 entries)
INSERT INTO Blood_Stock (blood_group, quantity, collection_date, expiry_date, storage_location, bank_id) VALUES
('A+', 25, '2025-09-10', '2025-10-22', 'Fridge A1', 1),
('O-', 15, '2025-09-08', '2025-10-20', 'Fridge A2', 1),
('B+', 20, '2025-09-11', '2025-10-23', 'Fridge B1', 2),
('AB+', 10, '2025-09-09', '2025-10-21', 'Fridge B2', 2),
('O+', 35, '2025-09-12', '2025-10-24', 'Fridge C1', 3),
('A-', 18, '2025-09-07', '2025-10-19', 'Fridge A1', 1),
('B-', 12, '2025-09-05', '2025-10-17', 'Fridge B1', 2),
('AB-', 8, '2025-09-06', '2025-10-18', 'Fridge C2', 3),
('A+', 22, '2025-09-13', '2025-10-25', 'Fridge A2', 1),
('O-', 14, '2025-09-14', '2025-10-26', 'Fridge B2', 2),
('B+', 28, '2025-09-04', '2025-10-16', 'Fridge C1', 3),
('O+', 40, '2025-09-15', '2025-10-27', 'Fridge A1', 1),
('A-', 10, '2025-09-03', '2025-10-15', 'Fridge B2', 2),
('B-', 16, '2025-09-02', '2025-10-14', 'Fridge C2', 3),
('AB+', 11, '2025-09-01', '2025-10-13', 'Fridge A2', 1);

-- Donation data (linking donors to stock)
INSERT INTO Donation (donor_id, unit_id, donation_date, quantity) VALUES
(1, 1, '2025-09-10', 1),
(2, 2, '2025-09-08', 1),
(3, 3, '2025-09-11', 1),
(4, 4, '2025-09-09', 1),
(5, 5, '2025-09-12', 1),
(6, 6, '2025-09-07', 1),
(7, 7, '2025-09-05', 1),
(8, 8, '2025-09-06', 1),
(9, 9, '2025-09-13', 1),
(10, 10, '2025-09-14', 1),
(11, 11, '2025-09-04', 1),
(12, 12, '2025-09-15', 1),
(13, 13, '2025-09-03', 1),
(14, 14, '2025-09-02', 1),
(15, 15, '2025-09-01', 1);
