-- Sample Data Insertion Script for Hospital Management System
-- This script populates the database with sample data for testing and demonstration

-- Insert sample doctors
INSERT OR IGNORE INTO doctors (first_name, last_name, specialization, phone, email, license_number, years_of_experience, consultation_fee) VALUES
('John', 'Smith', 'Cardiology', '555-1001', 'john.smith@hospital.com', 'MD001', 15, 200.00),
('Sarah', 'Johnson', 'Neurology', '555-1002', 'sarah.johnson@hospital.com', 'MD002', 12, 250.00),
('Michael', 'Brown', 'Orthopedics', '555-1003', 'michael.brown@hospital.com', 'MD003', 18, 180.00),
('Emily', 'Davis', 'Pediatrics', '555-1004', 'emily.davis@hospital.com', 'MD004', 10, 150.00),
('Robert', 'Wilson', 'Emergency Medicine', '555-1005', 'robert.wilson@hospital.com', 'MD005', 8, 220.00),
('Lisa', 'Anderson', 'Dermatology', '555-1006', 'lisa.anderson@hospital.com', 'MD006', 14, 160.00),
('David', 'Taylor', 'Psychiatry', '555-1007', 'david.taylor@hospital.com', 'MD007', 20, 300.00),
('Jennifer', 'Martinez', 'Radiology', '555-1008', 'jennifer.martinez@hospital.com', 'MD008', 16, 190.00);

-- Update departments with head doctors
UPDATE departments SET head_doctor_id = 1 WHERE department_name = 'Cardiology';
UPDATE departments SET head_doctor_id = 2 WHERE department_name = 'Neurology';
UPDATE departments SET head_doctor_id = 3 WHERE department_name = 'Orthopedics';
UPDATE departments SET head_doctor_id = 4 WHERE department_name = 'Pediatrics';
UPDATE departments SET head_doctor_id = 5 WHERE department_name = 'Emergency';

-- Insert sample patients
INSERT OR IGNORE INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, emergency_contact) VALUES
('Ahmed', 'Hassan', '1985-03-15', 'Male', '555-2001', 'ahmed.hassan@email.com', '123 Main St, Cairo', '555-2002'),
('Fatima', 'Ali', '1990-07-22', 'Female', '555-2003', 'fatima.ali@email.com', '456 Oak Ave, Alexandria', '555-2004'),
('Omar', 'Mohamed', '1978-11-08', 'Male', '555-2005', 'omar.mohamed@email.com', '789 Pine Rd, Giza', '555-2006'),
('Maryam', 'Ibrahim', '1995-02-14', 'Female', '555-2007', 'maryam.ibrahim@email.com', '321 Elm St, Cairo', '555-2008'),
('Youssef', 'Mahmoud', '1982-09-30', 'Male', '555-2009', 'youssef.mahmoud@email.com', '654 Maple Dr, Alexandria', '555-2010'),
('Nour', 'Ahmed', '1988-12-05', 'Female', '555-2011', 'nour.ahmed@email.com', '987 Cedar Ln, Giza', '555-2012'),
('Khaled', 'Farouk', '1975-06-18', 'Male', '555-2013', 'khaled.farouk@email.com', '147 Birch St, Cairo', '555-2014'),
('Amira', 'Salah', '1992-04-25', 'Female', '555-2015', 'amira.salah@email.com', '258 Walnut Ave, Alexandria', '555-2016'),
('Mahmoud', 'Nasser', '1980-01-12', 'Male', '555-2017', 'mahmoud.nasser@email.com', '369 Cherry Rd, Giza', '555-2018'),
('Yasmin', 'Kamal', '1993-08-07', 'Female', '555-2019', 'yasmin.kamal@email.com', '741 Spruce Dr, Cairo', '555-2020');

-- Insert sample appointments
INSERT OR IGNORE INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, appointment_type, notes) VALUES
(1, 1, '2024-01-15', '09:00', 'Completed', 'Consultation', 'Regular checkup for heart condition'),
(2, 4, '2024-01-16', '10:30', 'Completed', 'Consultation', 'Child vaccination'),
(3, 3, '2024-01-17', '14:00', 'Scheduled', 'Follow-up', 'Post-surgery checkup'),
(4, 2, '2024-01-18', '11:15', 'Scheduled', 'Consultation', 'Headache complaints'),
(5, 1, '2024-01-19', '15:30', 'Scheduled', 'Consultation', 'Chest pain evaluation'),
(6, 6, '2024-01-20', '09:45', 'Scheduled', 'Consultation', 'Skin rash examination'),
(7, 7, '2024-01-21', '13:00', 'Scheduled', 'Consultation', 'Anxiety treatment'),
(8, 8, '2024-01-22', '16:00', 'Scheduled', 'Procedure', 'MRI scan'),
(9, 5, '2024-01-23', '08:30', 'Scheduled', 'Emergency', 'Accident injury'),
(10, 4, '2024-01-24', '12:00', 'Scheduled', 'Consultation', 'Child development check');

-- Insert sample medical records
INSERT OR IGNORE INTO medical_records (patient_id, doctor_id, visit_date, chief_complaint, diagnosis, treatment, prescription, follow_up_date, notes) VALUES
(1, 1, '2024-01-15', 'Chest pain and shortness of breath', 'Mild hypertension', 'Lifestyle modifications, medication', 'Lisinopril 10mg once daily', '2024-02-15', 'Patient advised to reduce salt intake and exercise regularly'),
(2, 4, '2024-01-16', 'Routine vaccination', 'Healthy child', 'Vaccination administered', 'None', '2024-07-16', 'Next vaccination due in 6 months'),
(1, 1, '2023-12-10', 'Follow-up for hypertension', 'Controlled hypertension', 'Continue current medication', 'Lisinopril 10mg once daily', '2024-01-15', 'Blood pressure well controlled'),
(3, 3, '2023-11-20', 'Knee pain after fall', 'Mild knee sprain', 'Rest, ice, physiotherapy', 'Ibuprofen 400mg as needed', '2023-12-20', 'Patient responded well to treatment'),
(4, 2, '2023-10-05', 'Severe headaches', 'Tension headaches', 'Stress management, medication', 'Sumatriptan as needed', '2023-11-05', 'Headaches improved with treatment');

-- Insert sample staff
INSERT OR IGNORE INTO staff (first_name, last_name, role, department_id, phone, email, hire_date, salary, shift) VALUES
('Nurse', 'Ahmed', 'Registered Nurse', 1, '555-3001', 'nurse.ahmed@hospital.com', '2020-01-15', 45000.00, 'Morning'),
('Nurse', 'Fatma', 'Registered Nurse', 2, '555-3002', 'nurse.fatma@hospital.com', '2019-03-20', 47000.00, 'Evening'),
('Tech', 'Hassan', 'Lab Technician', NULL, '555-3003', 'tech.hassan@hospital.com', '2021-06-10', 35000.00, 'Morning'),
('Admin', 'Mona', 'Administrator', NULL, '555-3004', 'admin.mona@hospital.com', '2018-09-05', 55000.00, 'Morning'),
('Nurse', 'Karim', 'Registered Nurse', 3, '555-3005', 'nurse.karim@hospital.com', '2022-02-14', 46000.00, 'Night'),
('Tech', 'Layla', 'Radiology Technician', NULL, '555-3006', 'tech.layla@hospital.com', '2020-11-30', 40000.00, 'Morning');

-- Insert sample lab results
INSERT OR IGNORE INTO lab_results (patient_id, test_id, doctor_id, test_date, result_value, result_status, technician_notes, doctor_notes) VALUES
(1, 1, 1, '2024-01-15', 'WBC: 7,500/μL, RBC: 4.5M/μL, Platelets: 250,000/μL', 'Normal', 'All values within normal range', 'Good overall blood profile'),
(1, 2, 1, '2024-01-15', '95 mg/dL', 'Normal', 'Fasting glucose normal', 'No signs of diabetes'),
(3, 3, 3, '2023-11-20', 'No fractures visible, mild soft tissue swelling', 'Normal', 'Clear X-ray images obtained', 'Confirms clinical diagnosis of sprain'),
(4, 4, 2, '2023-10-05', 'Clear, yellow, no abnormal cells', 'Normal', 'Standard urine analysis performed', 'Rules out urinary tract issues'),
(5, 5, 1, '2024-01-19', 'Normal sinus rhythm, rate 72 bpm', 'Normal', 'Good quality ECG tracing', 'Normal cardiac rhythm');

-- Insert sample prescriptions (detailed)
INSERT OR IGNORE INTO prescriptions (record_id, medication_id, dosage, frequency, duration, instructions) VALUES
(1, 1, '500mg', 'Twice daily', '7 days', 'Take with food to avoid stomach upset'),
(1, 4, '75mg', 'Once daily', 'Ongoing', 'Take in the morning with breakfast'),
(3, 3, '400mg', 'As needed', '10 days', 'Take only when experiencing pain, maximum 3 times daily'),
(4, 1, '500mg', 'Three times daily', '5 days', 'Complete the full course even if symptoms improve'),
(5, 2, '250mg', 'Three times daily', '10 days', 'Take on empty stomach, 1 hour before meals');

-- Insert sample billing records
INSERT OR IGNORE INTO billing (patient_id, appointment_id, bill_date, total_amount, paid_amount, payment_status, payment_method, due_date) VALUES
(1, 1, '2024-01-15', 250.00, 250.00, 'Paid', 'Card', '2024-01-15'),
(2, 2, '2024-01-16', 180.00, 180.00, 'Paid', 'Cash', '2024-01-16'),
(3, 3, '2024-01-17', 200.00, 0.00, 'Pending', NULL, '2024-02-01'),
(4, 4, '2024-01-18', 280.00, 100.00, 'Partial', 'Card', '2024-02-02'),
(5, 5, '2024-01-19', 320.00, 0.00, 'Pending', NULL, '2024-02-03');

-- Insert sample admissions
INSERT OR IGNORE INTO admissions (patient_id, room_id, doctor_id, admission_date, discharge_date, admission_type, reason, status, total_cost) VALUES
(1, 3, 1, '2023-12-01 08:00:00', '2023-12-03 10:00:00', 'Elective', 'Cardiac monitoring', 'Discharged', 750.00),
(3, 1, 3, '2023-11-20 14:30:00', '2023-11-22 09:00:00', 'Emergency', 'Knee injury evaluation', 'Discharged', 450.00);

-- Update room occupancy based on current admissions
UPDATE rooms SET current_occupancy = 0, status = 'Available';

-- Sample data insertion completed successfully
-- The database now contains realistic sample data for testing the Hospital Management System
