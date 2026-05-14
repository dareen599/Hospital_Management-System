-- Hospital Management System Database Schema
-- This script creates the complete database structure for the hospital management system

-- Create database (SQLite will create automatically when connected)
-- For other databases, uncomment the following line:
-- CREATE DATABASE hospital_management;

-- Patients table - stores patient information
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE,
    gender TEXT CHECK(gender IN ('Male', 'Female')),
    phone TEXT,
    email TEXT,
    address TEXT,
    emergency_contact TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors table - stores doctor information
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    license_number TEXT UNIQUE NOT NULL,
    years_of_experience INTEGER,
    consultation_fee DECIMAL(10,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Departments table - stores hospital departments
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    head_doctor_id INTEGER,
    location TEXT,
    phone TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (head_doctor_id) REFERENCES doctors (doctor_id)
);

-- Appointments table - stores appointment information
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Completed', 'Cancelled', 'No-Show')),
    appointment_type TEXT DEFAULT 'Consultation',
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id) ON DELETE CASCADE
);

-- Medical records table - stores patient medical history
CREATE TABLE IF NOT EXISTS medical_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    visit_date DATE NOT NULL,
    chief_complaint TEXT,
    diagnosis TEXT,
    treatment TEXT,
    prescription TEXT,
    follow_up_date DATE,
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id) ON DELETE CASCADE
);

-- Medications table - stores medication information
CREATE TABLE IF NOT EXISTS medications (
    medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_name TEXT NOT NULL,
    generic_name TEXT,
    dosage_form TEXT, -- tablet, capsule, syrup, injection, etc.
    strength TEXT,
    manufacturer TEXT,
    price DECIMAL(10,2),
    stock_quantity INTEGER DEFAULT 0,
    expiry_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prescriptions table - detailed prescription information
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT NOT NULL, -- e.g., "3 times daily", "twice daily"
    duration TEXT NOT NULL, -- e.g., "7 days", "2 weeks"
    instructions TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES medical_records (record_id) ON DELETE CASCADE,
    FOREIGN KEY (medication_id) REFERENCES medications (medication_id)
);

-- Staff table - stores hospital staff information
CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL, -- nurse, technician, administrator, etc.
    department_id INTEGER,
    phone TEXT,
    email TEXT UNIQUE,
    hire_date DATE,
    salary DECIMAL(10,2),
    shift TEXT, -- morning, evening, night
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

-- Rooms table - stores hospital room information
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT NOT NULL UNIQUE,
    room_type TEXT NOT NULL, -- ICU, General, Private, Semi-Private, Emergency
    floor_number INTEGER,
    capacity INTEGER DEFAULT 1,
    current_occupancy INTEGER DEFAULT 0,
    daily_rate DECIMAL(10,2),
    status TEXT DEFAULT 'Available' CHECK(status IN ('Available', 'Occupied', 'Maintenance', 'Reserved')),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patient admissions table - tracks patient hospital stays
CREATE TABLE IF NOT EXISTS admissions (
    admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    admission_date DATETIME NOT NULL,
    discharge_date DATETIME,
    admission_type TEXT, -- Emergency, Elective, Transfer
    reason TEXT,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Discharged', 'Transferred')),
    total_cost DECIMAL(10,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms (room_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
);

-- Billing table - stores billing information
CREATE TABLE IF NOT EXISTS billing (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    admission_id INTEGER,
    appointment_id INTEGER,
    bill_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    payment_status TEXT DEFAULT 'Pending' CHECK(payment_status IN ('Pending', 'Partial', 'Paid', 'Overdue')),
    payment_method TEXT, -- Cash, Card, Insurance, Bank Transfer
    insurance_claim_number TEXT,
    due_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE,
    FOREIGN KEY (admission_id) REFERENCES admissions (admission_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
);

-- Lab tests table - stores laboratory test information
CREATE TABLE IF NOT EXISTS lab_tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT NOT NULL,
    test_category TEXT, -- Blood, Urine, X-Ray, MRI, CT Scan, etc.
    normal_range TEXT,
    cost DECIMAL(10,2),
    preparation_instructions TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patient lab results table
CREATE TABLE IF NOT EXISTS lab_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    test_date DATE NOT NULL,
    result_value TEXT,
    result_status TEXT, -- Normal, Abnormal, Critical
    technician_notes TEXT,
    doctor_notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES lab_tests (test_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name);
CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors(specialization);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_medical_records_patient ON medical_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_medical_records_date ON medical_records(visit_date);
CREATE INDEX IF NOT EXISTS idx_admissions_patient ON admissions(patient_id);
CREATE INDEX IF NOT EXISTS idx_billing_patient ON billing(patient_id);
CREATE INDEX IF NOT EXISTS idx_lab_results_patient ON lab_results(patient_id);

-- Create triggers for updating timestamps
CREATE TRIGGER IF NOT EXISTS update_patients_timestamp 
    AFTER UPDATE ON patients
    BEGIN
        UPDATE patients SET updated_date = CURRENT_TIMESTAMP WHERE patient_id = NEW.patient_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_doctors_timestamp 
    AFTER UPDATE ON doctors
    BEGIN
        UPDATE doctors SET updated_date = CURRENT_TIMESTAMP WHERE doctor_id = NEW.doctor_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_appointments_timestamp 
    AFTER UPDATE ON appointments
    BEGIN
        UPDATE appointments SET updated_date = CURRENT_TIMESTAMP WHERE appointment_id = NEW.appointment_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_medical_records_timestamp 
    AFTER UPDATE ON medical_records
    BEGIN
        UPDATE medical_records SET updated_date = CURRENT_TIMESTAMP WHERE record_id = NEW.record_id;
    END;

-- Create views for commonly used queries
CREATE VIEW IF NOT EXISTS patient_summary AS
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS full_name,
    p.date_of_birth,
    p.gender,
    p.phone,
    p.email,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT mr.record_id) AS total_records,
    MAX(a.appointment_date) AS last_appointment_date
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
LEFT JOIN medical_records mr ON p.patient_id = mr.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name, p.date_of_birth, p.gender, p.phone, p.email;

CREATE VIEW IF NOT EXISTS doctor_summary AS
SELECT 
    d.doctor_id,
    d.first_name || ' ' || d.last_name AS full_name,
    d.specialization,
    d.phone,
    d.email,
    d.license_number,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT mr.record_id) AS total_consultations
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
LEFT JOIN medical_records mr ON d.doctor_id = mr.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization, d.phone, d.email, d.license_number;

CREATE VIEW IF NOT EXISTS appointment_details AS
SELECT 
    a.appointment_id,
    p.first_name || ' ' || p.last_name AS patient_name,
    d.first_name || ' ' || d.last_name AS doctor_name,
    d.specialization,
    a.appointment_date,
    a.appointment_time,
    a.status,
    a.appointment_type,
    a.notes
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;

-- Insert some sample data for testing
INSERT OR IGNORE INTO departments (department_name, location, phone) VALUES
('Cardiology', 'Building A, Floor 2', '555-0101'),
('Neurology', 'Building B, Floor 3', '555-0102'),
('Orthopedics', 'Building A, Floor 1', '555-0103'),
('Pediatrics', 'Building C, Floor 2', '555-0104'),
('Emergency', 'Building A, Ground Floor', '555-0105');

INSERT OR IGNORE INTO medications (medication_name, generic_name, dosage_form, strength, manufacturer, price, stock_quantity) VALUES
('Paracetamol', 'Acetaminophen', 'Tablet', '500mg', 'PharmaCorp', 0.50, 1000),
('Amoxicillin', 'Amoxicillin', 'Capsule', '250mg', 'MediLab', 2.00, 500),
('Ibuprofen', 'Ibuprofen', 'Tablet', '400mg', 'HealthPlus', 0.75, 800),
('Aspirin', 'Acetylsalicylic Acid', 'Tablet', '75mg', 'CardioMed', 0.25, 1200),
('Omeprazole', 'Omeprazole', 'Capsule', '20mg', 'GastroHealth', 1.50, 300);

INSERT OR IGNORE INTO lab_tests (test_name, test_category, normal_range, cost, preparation_instructions) VALUES
('Complete Blood Count', 'Blood', 'WBC: 4,000-11,000/μL', 25.00, 'No special preparation required'),
('Blood Glucose', 'Blood', '70-100 mg/dL (fasting)', 15.00, 'Fast for 8-12 hours before test'),
('Chest X-Ray', 'Radiology', 'Normal lung fields', 50.00, 'Remove jewelry and metal objects'),
('Urine Analysis', 'Urine', 'Clear, yellow color', 20.00, 'Clean catch midstream sample'),
('ECG', 'Cardiac', 'Normal sinus rhythm', 30.00, 'Avoid caffeine 2 hours before test');

INSERT OR IGNORE INTO rooms (room_number, room_type, floor_number, capacity, daily_rate, status) VALUES
('101', 'General', 1, 2, 150.00, 'Available'),
('102', 'General', 1, 2, 150.00, 'Available'),
('201', 'Private', 2, 1, 250.00, 'Available'),
('202', 'Private', 2, 1, 250.00, 'Available'),
('301', 'ICU', 3, 1, 500.00, 'Available'),
('302', 'ICU', 3, 1, 500.00, 'Available'),
('ER1', 'Emergency', 0, 1, 200.00, 'Available'),
('ER2', 'Emergency', 0, 1, 200.00, 'Available');

-- Database schema creation completed successfully
-- The database is now ready for use with the Hospital Management System
