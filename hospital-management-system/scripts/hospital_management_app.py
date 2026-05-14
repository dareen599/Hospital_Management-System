import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime, date
import os

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.init_database()
        
        # Create main interface
        self.create_main_interface()
        
    def init_database(self):
        """Initialize SQLite database connection"""
        self.conn = sqlite3.connect('hospital_management.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.create_tables()
        
    def create_tables(self):
        """Create database tables"""
        # Patients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE,
                gender TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                emergency_contact TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Doctors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialization TEXT,
                phone TEXT,
                email TEXT,
                license_number TEXT UNIQUE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                appointment_date DATE,
                appointment_time TIME,
                status TEXT DEFAULT 'Scheduled',
                notes TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
            )
        ''')
        
        # Medical records table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                visit_date DATE,
                diagnosis TEXT,
                treatment TEXT,
                prescription TEXT,
                notes TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
            )
        ''')
        
        self.conn.commit()
        
    def create_main_interface(self):
        """Create the main application interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Hospital Management System", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        self.create_medical_records_tab()
        self.create_dashboard_tab()
        
    def create_patients_tab(self):
        """Create patients management tab"""
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="Patients")
        
        # Patients form frame
        form_frame = tk.LabelFrame(patients_frame, text="Patient Information", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.patient_first_name = tk.Entry(form_frame, width=20)
        self.patient_first_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Last Name:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.patient_last_name = tk.Entry(form_frame, width=20)
        self.patient_last_name.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Date of Birth:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.patient_dob = tk.Entry(form_frame, width=20)
        self.patient_dob.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Gender:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.patient_gender = ttk.Combobox(form_frame, values=['Male', 'Female'], width=17)
        self.patient_gender.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.patient_phone = tk.Entry(form_frame, width=20)
        self.patient_phone.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Email:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.patient_email = tk.Entry(form_frame, width=20)
        self.patient_email.grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.patient_address = tk.Entry(form_frame, width=50)
        self.patient_address.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        tk.Button(buttons_frame, text="Add Patient", command=self.add_patient,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Update Patient", command=self.update_patient,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Delete Patient", command=self.delete_patient,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Clear Form", command=self.clear_patient_form,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Patients list frame
        list_frame = tk.LabelFrame(patients_frame, text="Patients List", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for patients list
        columns = ('ID', 'First Name', 'Last Name', 'DOB', 'Gender', 'Phone', 'Email')
        self.patients_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120)
        
        # Scrollbar for treeview
        scrollbar_patients = ttk.Scrollbar(list_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar_patients.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        scrollbar_patients.pack(side='right', fill='y')
        
        # Bind selection event
        self.patients_tree.bind('<<TreeviewSelect>>', self.on_patient_select)
        
        # Load patients data
        self.load_patients()
        
    def create_doctors_tab(self):
        """Create doctors management tab"""
        doctors_frame = ttk.Frame(self.notebook)
        self.notebook.add(doctors_frame, text="Doctors")
        
        # Doctors form frame
        form_frame = tk.LabelFrame(doctors_frame, text="Doctor Information", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.doctor_first_name = tk.Entry(form_frame, width=20)
        self.doctor_first_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Last Name:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.doctor_last_name = tk.Entry(form_frame, width=20)
        self.doctor_last_name.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Specialization:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.doctor_specialization = ttk.Combobox(form_frame, values=[
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology',
            'Psychiatry', 'Radiology', 'Surgery', 'Internal Medicine', 'Emergency Medicine'
        ], width=17)
        self.doctor_specialization.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Phone:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.doctor_phone = tk.Entry(form_frame, width=20)
        self.doctor_phone.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.doctor_email = tk.Entry(form_frame, width=20)
        self.doctor_email.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="License Number:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.doctor_license = tk.Entry(form_frame, width=20)
        self.doctor_license.grid(row=2, column=3, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Button(buttons_frame, text="Add Doctor", command=self.add_doctor,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Update Doctor", command=self.update_doctor,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Delete Doctor", command=self.delete_doctor,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Clear Form", command=self.clear_doctor_form,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Doctors list frame
        list_frame = tk.LabelFrame(doctors_frame, text="Doctors List", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for doctors list
        columns = ('ID', 'First Name', 'Last Name', 'Specialization', 'Phone', 'Email', 'License')
        self.doctors_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=120)
        
        # Scrollbar for treeview
        scrollbar_doctors = ttk.Scrollbar(list_frame, orient='vertical', command=self.doctors_tree.yview)
        self.doctors_tree.configure(yscrollcommand=scrollbar_doctors.set)
        
        self.doctors_tree.pack(side='left', fill='both', expand=True)
        scrollbar_doctors.pack(side='right', fill='y')
        
        # Bind selection event
        self.doctors_tree.bind('<<TreeviewSelect>>', self.on_doctor_select)
        
        # Load doctors data
        self.load_doctors()
        
    def create_appointments_tab(self):
        """Create appointments management tab"""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="Appointments")
        
        # Appointments form frame
        form_frame = tk.LabelFrame(appointments_frame, text="Appointment Information", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="Patient:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.appointment_patient = ttk.Combobox(form_frame, width=25)
        self.appointment_patient.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Doctor:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.appointment_doctor = ttk.Combobox(form_frame, width=25)
        self.appointment_doctor.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.appointment_date = tk.Entry(form_frame, width=20)
        self.appointment_date.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Time (HH:MM):").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.appointment_time = tk.Entry(form_frame, width=20)
        self.appointment_time.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Status:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.appointment_status = ttk.Combobox(form_frame, values=['Scheduled', 'Completed', 'Cancelled'], width=17)
        self.appointment_status.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Notes:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.appointment_notes = tk.Entry(form_frame, width=30)
        self.appointment_notes.grid(row=2, column=3, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        tk.Button(buttons_frame, text="Schedule Appointment", command=self.add_appointment,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Update Appointment", command=self.update_appointment,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Cancel Appointment", command=self.delete_appointment,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Clear Form", command=self.clear_appointment_form,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Appointments list frame
        list_frame = tk.LabelFrame(appointments_frame, text="Appointments List", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for appointments list
        columns = ('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status', 'Notes')
        self.appointments_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        # Scrollbar for treeview
        scrollbar_appointments = ttk.Scrollbar(list_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar_appointments.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar_appointments.pack(side='right', fill='y')
        
        # Bind selection event
        self.appointments_tree.bind('<<TreeviewSelect>>', self.on_appointment_select)
        
        # Load appointments data
        self.load_appointments()
        self.load_patients_doctors_for_appointments()
        
    def create_medical_records_tab(self):
        """Create medical records management tab"""
        records_frame = ttk.Frame(self.notebook)
        self.notebook.add(records_frame, text="Medical Records")
        
        # Medical records form frame
        form_frame = tk.LabelFrame(records_frame, text="Medical Record Information", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Form fields
        tk.Label(form_frame, text="Patient:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.record_patient = ttk.Combobox(form_frame, width=25)
        self.record_patient.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Doctor:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.record_doctor = ttk.Combobox(form_frame, width=25)
        self.record_doctor.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Visit Date:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.record_date = tk.Entry(form_frame, width=20)
        self.record_date.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Diagnosis:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.record_diagnosis = tk.Text(form_frame, width=30, height=3)
        self.record_diagnosis.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Treatment:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.record_treatment = tk.Text(form_frame, width=30, height=3)
        self.record_treatment.grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(form_frame, text="Prescription:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.record_prescription = tk.Text(form_frame, width=30, height=3)
        self.record_prescription.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Notes:").grid(row=3, column=2, sticky='w', padx=5, pady=5)
        self.record_notes = tk.Text(form_frame, width=30, height=3)
        self.record_notes.grid(row=3, column=3, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        tk.Button(buttons_frame, text="Add Record", command=self.add_medical_record,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Update Record", command=self.update_medical_record,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Delete Record", command=self.delete_medical_record,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(buttons_frame, text="Clear Form", command=self.clear_medical_record_form,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Medical records list frame
        list_frame = tk.LabelFrame(records_frame, text="Medical Records List", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for medical records list
        columns = ('ID', 'Patient', 'Doctor', 'Visit Date', 'Diagnosis')
        self.records_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=150)
        
        # Scrollbar for treeview
        scrollbar_records = ttk.Scrollbar(list_frame, orient='vertical', command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar_records.set)
        
        self.records_tree.pack(side='left', fill='both', expand=True)
        scrollbar_records.pack(side='right', fill='y')
        
        # Bind selection event
        self.records_tree.bind('<<TreeviewSelect>>', self.on_record_select)
        
        # Load medical records data
        self.load_medical_records()
        self.load_patients_doctors_for_records()
        
    def create_dashboard_tab(self):
        """Create dashboard tab with statistics"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Statistics frame
        stats_frame = tk.LabelFrame(dashboard_frame, text="Hospital Statistics", 
                                   font=('Arial', 14, 'bold'), padx=20, pady=20)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Create statistics labels
        self.stats_patients = tk.Label(stats_frame, text="Total Patients: 0", 
                                      font=('Arial', 12), bg='#3498db', fg='white', 
                                      padx=20, pady=10)
        self.stats_patients.grid(row=0, column=0, padx=10, pady=10)
        
        self.stats_doctors = tk.Label(stats_frame, text="Total Doctors: 0", 
                                     font=('Arial', 12), bg='#2ecc71', fg='white', 
                                     padx=20, pady=10)
        self.stats_doctors.grid(row=0, column=1, padx=10, pady=10)
        
        self.stats_appointments = tk.Label(stats_frame, text="Total Appointments: 0", 
                                          font=('Arial', 12), bg='#f39c12', fg='white', 
                                          padx=20, pady=10)
        self.stats_appointments.grid(row=0, column=2, padx=10, pady=10)
        
        self.stats_records = tk.Label(stats_frame, text="Medical Records: 0", 
                                     font=('Arial', 12), bg='#9b59b6', fg='white', 
                                     padx=20, pady=10)
        self.stats_records.grid(row=0, column=3, padx=10, pady=10)
        
        # Recent activities frame
        activities_frame = tk.LabelFrame(dashboard_frame, text="Recent Activities", 
                                        font=('Arial', 14, 'bold'), padx=20, pady=20)
        activities_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Activities text widget
        self.activities_text = tk.Text(activities_frame, height=20, font=('Arial', 10))
        activities_scrollbar = ttk.Scrollbar(activities_frame, orient='vertical', 
                                           command=self.activities_text.yview)
        self.activities_text.configure(yscrollcommand=activities_scrollbar.set)
        
        self.activities_text.pack(side='left', fill='both', expand=True)
        activities_scrollbar.pack(side='right', fill='y')
        
        # Refresh button
        refresh_btn = tk.Button(dashboard_frame, text="Refresh Dashboard", 
                               command=self.refresh_dashboard,
                               bg='#34495e', fg='white', font=('Arial', 12, 'bold'))
        refresh_btn.pack(pady=10)
        
        # Load dashboard data
        self.refresh_dashboard()
    
    # Patient management methods
    def add_patient(self):
        """Add new patient to database"""
        try:
            self.cursor.execute('''
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, 
                                    phone, email, address, emergency_contact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.patient_first_name.get(),
                self.patient_last_name.get(),
                self.patient_dob.get(),
                self.patient_gender.get(),
                self.patient_phone.get(),
                self.patient_email.get(),
                self.patient_address.get(),
                self.patient_phone.get()  # Using phone as emergency contact for simplicity
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
            self.clear_patient_form()
            self.load_patients()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding patient: {str(e)}")
    
    def update_patient(self):
        """Update selected patient"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to update")
            return
        
        try:
            patient_id = self.patients_tree.item(selected[0])['values'][0]
            self.cursor.execute('''
                UPDATE patients SET first_name=?, last_name=?, date_of_birth=?, 
                                  gender=?, phone=?, email=?, address=?
                WHERE patient_id=?
            ''', (
                self.patient_first_name.get(),
                self.patient_last_name.get(),
                self.patient_dob.get(),
                self.patient_gender.get(),
                self.patient_phone.get(),
                self.patient_email.get(),
                self.patient_address.get(),
                patient_id
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.clear_patient_form()
            self.load_patients()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating patient: {str(e)}")
    
    def delete_patient(self):
        """Delete selected patient"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            try:
                patient_id = self.patients_tree.item(selected[0])['values'][0]
                self.cursor.execute('DELETE FROM patients WHERE patient_id=?', (patient_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Patient deleted successfully!")
                self.clear_patient_form()
                self.load_patients()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting patient: {str(e)}")
    
    def clear_patient_form(self):
        """Clear patient form fields"""
        self.patient_first_name.delete(0, tk.END)
        self.patient_last_name.delete(0, tk.END)
        self.patient_dob.delete(0, tk.END)
        self.patient_gender.set('')
        self.patient_phone.delete(0, tk.END)
        self.patient_email.delete(0, tk.END)
        self.patient_address.delete(0, tk.END)
    
    def on_patient_select(self, event):
        """Handle patient selection"""
        selected = self.patients_tree.selection()
        if selected:
            values = self.patients_tree.item(selected[0])['values']
            self.patient_first_name.delete(0, tk.END)
            self.patient_first_name.insert(0, values[1])
            self.patient_last_name.delete(0, tk.END)
            self.patient_last_name.insert(0, values[2])
            self.patient_dob.delete(0, tk.END)
            self.patient_dob.insert(0, values[3])
            self.patient_gender.set(values[4])
            self.patient_phone.delete(0, tk.END)
            self.patient_phone.insert(0, values[5])
            self.patient_email.delete(0, tk.END)
            self.patient_email.insert(0, values[6])
    
    def load_patients(self):
        """Load patients data into treeview"""
        # Clear existing data
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Fetch and display patients
        self.cursor.execute('SELECT * FROM patients ORDER BY patient_id')
        patients = self.cursor.fetchall()
        
        for patient in patients:
            self.patients_tree.insert('', 'end', values=patient[:7])  # Exclude address and emergency_contact
    
    # Doctor management methods (similar structure to patients)
    def add_doctor(self):
        """Add new doctor to database"""
        try:
            self.cursor.execute('''
                INSERT INTO doctors (first_name, last_name, specialization, phone, email, license_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.doctor_first_name.get(),
                self.doctor_last_name.get(),
                self.doctor_specialization.get(),
                self.doctor_phone.get(),
                self.doctor_email.get(),
                self.doctor_license.get()
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            self.clear_doctor_form()
            self.load_doctors()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding doctor: {str(e)}")
    
    def update_doctor(self):
        """Update selected doctor"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to update")
            return
        
        try:
            doctor_id = self.doctors_tree.item(selected[0])['values'][0]
            self.cursor.execute('''
                UPDATE doctors SET first_name=?, last_name=?, specialization=?, 
                                 phone=?, email=?, license_number=?
                WHERE doctor_id=?
            ''', (
                self.doctor_first_name.get(),
                self.doctor_last_name.get(),
                self.doctor_specialization.get(),
                self.doctor_phone.get(),
                self.doctor_email.get(),
                self.doctor_license.get(),
                doctor_id
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            self.clear_doctor_form()
            self.load_doctors()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating doctor: {str(e)}")
    
    def delete_doctor(self):
        """Delete selected doctor"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            try:
                doctor_id = self.doctors_tree.item(selected[0])['values'][0]
                self.cursor.execute('DELETE FROM doctors WHERE doctor_id=?', (doctor_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.clear_doctor_form()
                self.load_doctors()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting doctor: {str(e)}")
    
    def clear_doctor_form(self):
        """Clear doctor form fields"""
        self.doctor_first_name.delete(0, tk.END)
        self.doctor_last_name.delete(0, tk.END)
        self.doctor_specialization.set('')
        self.doctor_phone.delete(0, tk.END)
        self.doctor_email.delete(0, tk.END)
        self.doctor_license.delete(0, tk.END)
    
    def on_doctor_select(self, event):
        """Handle doctor selection"""
        selected = self.doctors_tree.selection()
        if selected:
            values = self.doctors_tree.item(selected[0])['values']
            self.doctor_first_name.delete(0, tk.END)
            self.doctor_first_name.insert(0, values[1])
            self.doctor_last_name.delete(0, tk.END)
            self.doctor_last_name.insert(0, values[2])
            self.doctor_specialization.set(values[3])
            self.doctor_phone.delete(0, tk.END)
            self.doctor_phone.insert(0, values[4])
            self.doctor_email.delete(0, tk.END)
            self.doctor_email.insert(0, values[5])
            self.doctor_license.delete(0, tk.END)
            self.doctor_license.insert(0, values[6])
    
    def load_doctors(self):
        """Load doctors data into treeview"""
        # Clear existing data
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
        
        # Fetch and display doctors
        self.cursor.execute('SELECT * FROM doctors ORDER BY doctor_id')
        doctors = self.cursor.fetchall()
        
        for doctor in doctors:
            self.doctors_tree.insert('', 'end', values=doctor[:7])
    
    # Appointment management methods
    def add_appointment(self):
        """Add new appointment"""
        try:
            patient_text = self.appointment_patient.get()
            doctor_text = self.appointment_doctor.get()
            
            if not patient_text or not doctor_text:
                messagebox.showwarning("Warning", "Please select both patient and doctor")
                return
            
            patient_id = patient_text.split(' - ')[0]
            doctor_id = doctor_text.split(' - ')[0]
            
            self.cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, 
                                        appointment_time, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                patient_id,
                doctor_id,
                self.appointment_date.get(),
                self.appointment_time.get(),
                self.appointment_status.get() or 'Scheduled',
                self.appointment_notes.get()
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Appointment scheduled successfully!")
            self.clear_appointment_form()
            self.load_appointments()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error scheduling appointment: {str(e)}")
    
    def update_appointment(self):
        """Update selected appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return
        
        try:
            appointment_id = self.appointments_tree.item(selected[0])['values'][0]
            patient_text = self.appointment_patient.get()
            doctor_text = self.appointment_doctor.get()
            
            patient_id = patient_text.split(' - ')[0]
            doctor_id = doctor_text.split(' - ')[0]
            
            self.cursor.execute('''
                UPDATE appointments SET patient_id=?, doctor_id=?, appointment_date=?, 
                                     appointment_time=?, status=?, notes=?
                WHERE appointment_id=?
            ''', (
                patient_id,
                doctor_id,
                self.appointment_date.get(),
                self.appointment_time.get(),
                self.appointment_status.get(),
                self.appointment_notes.get(),
                appointment_id
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Appointment updated successfully!")
            self.clear_appointment_form()
            self.load_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating appointment: {str(e)}")
    
    def delete_appointment(self):
        """Delete selected appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            try:
                appointment_id = self.appointments_tree.item(selected[0])['values'][0]
                self.cursor.execute('DELETE FROM appointments WHERE appointment_id=?', (appointment_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Appointment cancelled successfully!")
                self.clear_appointment_form()
                self.load_appointments()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error cancelling appointment: {str(e)}")
    
    def clear_appointment_form(self):
        """Clear appointment form fields"""
        self.appointment_patient.set('')
        self.appointment_doctor.set('')
        self.appointment_date.delete(0, tk.END)
        self.appointment_time.delete(0, tk.END)
        self.appointment_status.set('')
        self.appointment_notes.delete(0, tk.END)
    
    def on_appointment_select(self, event):
        """Handle appointment selection"""
        selected = self.appointments_tree.selection()
        if selected:
            values = self.appointments_tree.item(selected[0])['values']
            # Set patient and doctor comboboxes
            self.appointment_patient.set(values[1])
            self.appointment_doctor.set(values[2])
            self.appointment_date.delete(0, tk.END)
            self.appointment_date.insert(0, values[3])
            self.appointment_time.delete(0, tk.END)
            self.appointment_time.insert(0, values[4])
            self.appointment_status.set(values[5])
            self.appointment_notes.delete(0, tk.END)
            self.appointment_notes.insert(0, values[6])
    
    def load_appointments(self):
        """Load appointments data into treeview"""
        # Clear existing data
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Fetch and display appointments with patient and doctor names
        self.cursor.execute('''
            SELECT a.appointment_id, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   a.appointment_date, a.appointment_time, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date, a.appointment_time
        ''')
        appointments = self.cursor.fetchall()
        
        for appointment in appointments:
            self.appointments_tree.insert('', 'end', values=appointment)
    
    def load_patients_doctors_for_appointments(self):
        """Load patients and doctors for appointment comboboxes"""
        # Load patients
        self.cursor.execute('SELECT patient_id, first_name, last_name FROM patients')
        patients = self.cursor.fetchall()
        patient_list = [f"{p[0]} - {p[1]} {p[2]}" for p in patients]
        self.appointment_patient['values'] = patient_list
        
        # Load doctors
        self.cursor.execute('SELECT doctor_id, first_name, last_name, specialization FROM doctors')
        doctors = self.cursor.fetchall()
        doctor_list = [f"{d[0]} - Dr. {d[1]} {d[2]} ({d[3]})" for d in doctors]
        self.appointment_doctor['values'] = doctor_list
    
    # Medical records management methods
    def add_medical_record(self):
        """Add new medical record"""
        try:
            patient_text = self.record_patient.get()
            doctor_text = self.record_doctor.get()
            
            if not patient_text or not doctor_text:
                messagebox.showwarning("Warning", "Please select both patient and doctor")
                return
            
            patient_id = patient_text.split(' - ')[0]
            doctor_id = doctor_text.split(' - ')[0]
            
            self.cursor.execute('''
                INSERT INTO medical_records (patient_id, doctor_id, visit_date, 
                                           diagnosis, treatment, prescription, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_id,
                doctor_id,
                self.record_date.get(),
                self.record_diagnosis.get('1.0', tk.END).strip(),
                self.record_treatment.get('1.0', tk.END).strip(),
                self.record_prescription.get('1.0', tk.END).strip(),
                self.record_notes.get('1.0', tk.END).strip()
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Medical record added successfully!")
            self.clear_medical_record_form()
            self.load_medical_records()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding medical record: {str(e)}")
    
    def update_medical_record(self):
        """Update selected medical record"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medical record to update")
            return
        
        try:
            record_id = self.records_tree.item(selected[0])['values'][0]
            patient_text = self.record_patient.get()
            doctor_text = self.record_doctor.get()
            
            patient_id = patient_text.split(' - ')[0]
            doctor_id = doctor_text.split(' - ')[0]
            
            self.cursor.execute('''
                UPDATE medical_records SET patient_id=?, doctor_id=?, visit_date=?, 
                                         diagnosis=?, treatment=?, prescription=?, notes=?
                WHERE record_id=?
            ''', (
                patient_id,
                doctor_id,
                self.record_date.get(),
                self.record_diagnosis.get('1.0', tk.END).strip(),
                self.record_treatment.get('1.0', tk.END).strip(),
                self.record_prescription.get('1.0', tk.END).strip(),
                self.record_notes.get('1.0', tk.END).strip(),
                record_id
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Medical record updated successfully!")
            self.clear_medical_record_form()
            self.load_medical_records()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating medical record: {str(e)}")
    
    def delete_medical_record(self):
        """Delete selected medical record"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medical record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this medical record?"):
            try:
                record_id = self.records_tree.item(selected[0])['values'][0]
                self.cursor.execute('DELETE FROM medical_records WHERE record_id=?', (record_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Medical record deleted successfully!")
                self.clear_medical_record_form()
                self.load_medical_records()
                self.refresh_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting medical record: {str(e)}")
    
    def clear_medical_record_form(self):
        """Clear medical record form fields"""
        self.record_patient.set('')
        self.record_doctor.set('')
        self.record_date.delete(0, tk.END)
        self.record_diagnosis.delete('1.0', tk.END)
        self.record_treatment.delete('1.0', tk.END)
        self.record_prescription.delete('1.0', tk.END)
        self.record_notes.delete('1.0', tk.END)
    
    def on_record_select(self, event):
        """Handle medical record selection"""
        selected = self.records_tree.selection()
        if selected:
            values = self.records_tree.item(selected[0])['values']
            # Get full record details
            record_id = values[0]
            self.cursor.execute('''
                SELECT mr.*, p.first_name || ' ' || p.last_name as patient_name,
                       d.first_name || ' ' || d.last_name as doctor_name
                FROM medical_records mr
                JOIN patients p ON mr.patient_id = p.patient_id
                JOIN doctors d ON mr.doctor_id = d.doctor_id
                WHERE mr.record_id = ?
            ''', (record_id,))
            record = self.cursor.fetchone()
            
            if record:
                self.record_patient.set(f"{record[1]} - {record[9]}")
                self.record_doctor.set(f"{record[2]} - {record[10]}")
                self.record_date.delete(0, tk.END)
                self.record_date.insert(0, record[3])
                self.record_diagnosis.delete('1.0', tk.END)
                self.record_diagnosis.insert('1.0', record[4] or '')
                self.record_treatment.delete('1.0', tk.END)
                self.record_treatment.insert('1.0', record[5] or '')
                self.record_prescription.delete('1.0', tk.END)
                self.record_prescription.insert('1.0', record[6] or '')
                self.record_notes.delete('1.0', tk.END)
                self.record_notes.insert('1.0', record[7] or '')
    
    def load_medical_records(self):
        """Load medical records data into treeview"""
        # Clear existing data
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        # Fetch and display medical records with patient and doctor names
        self.cursor.execute('''
            SELECT mr.record_id, 
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   mr.visit_date, mr.diagnosis
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            ORDER BY mr.visit_date DESC
        ''')
        records = self.cursor.fetchall()
        
        for record in records:
            # Truncate diagnosis if too long
            diagnosis = record[4][:50] + "..." if len(record[4]) > 50 else record[4]
            display_record = list(record[:4]) + [diagnosis]
            self.records_tree.insert('', 'end', values=display_record)
    
    def load_patients_doctors_for_records(self):
        """Load patients and doctors for medical record comboboxes"""
        # Load patients
        self.cursor.execute('SELECT patient_id, first_name, last_name FROM patients')
        patients = self.cursor.fetchall()
        patient_list = [f"{p[0]} - {p[1]} {p[2]}" for p in patients]
        self.record_patient['values'] = patient_list
        
        # Load doctors
        self.cursor.execute('SELECT doctor_id, first_name, last_name, specialization FROM doctors')
        doctors = self.cursor.fetchall()
        doctor_list = [f"{d[0]} - Dr. {d[1]} {d[2]} ({d[3]})" for d in doctors]
        self.record_doctor['values'] = doctor_list
    
    # Dashboard methods
    def refresh_dashboard(self):
        """Refresh dashboard statistics and activities"""
        # Update statistics
        self.cursor.execute('SELECT COUNT(*) FROM patients')
        patients_count = self.cursor.fetchone()[0]
        self.stats_patients.config(text=f"Total Patients: {patients_count}")
        
        self.cursor.execute('SELECT COUNT(*) FROM doctors')
        doctors_count = self.cursor.fetchone()[0]
        self.stats_doctors.config(text=f"Total Doctors: {doctors_count}")
        
        self.cursor.execute('SELECT COUNT(*) FROM appointments')
        appointments_count = self.cursor.fetchone()[0]
        self.stats_appointments.config(text=f"Total Appointments: {appointments_count}")
        
        self.cursor.execute('SELECT COUNT(*) FROM medical_records')
        records_count = self.cursor.fetchone()[0]
        self.stats_records.config(text=f"Medical Records: {records_count}")
        
        # Update recent activities
        self.activities_text.delete('1.0', tk.END)
        
        # Recent appointments
        self.cursor.execute('''
            SELECT a.appointment_date, a.appointment_time,
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.created_date DESC
            LIMIT 10
        ''')
        recent_appointments = self.cursor.fetchall()
        
        self.activities_text.insert(tk.END, "RECENT APPOINTMENTS:\n")
        self.activities_text.insert(tk.END, "=" * 50 + "\n")
        for apt in recent_appointments:
            self.activities_text.insert(tk.END, 
                f"• {apt[0]} {apt[1]} - {apt[2]} with Dr. {apt[3]} ({apt[4]})\n")
        
        # Recent medical records
        self.cursor.execute('''
            SELECT mr.visit_date,
                   p.first_name || ' ' || p.last_name as patient_name,
                   d.first_name || ' ' || d.last_name as doctor_name,
                   mr.diagnosis
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            ORDER BY mr.created_date DESC
            LIMIT 5
        ''')
        recent_records = self.cursor.fetchall()
        
        self.activities_text.insert(tk.END, "\n\nRECENT MEDICAL RECORDS:\n")
        self.activities_text.insert(tk.END, "=" * 50 + "\n")
        for record in recent_records:
            diagnosis = record[3][:40] + "..." if len(record[3]) > 40 else record[3]
            self.activities_text.insert(tk.END, 
                f"• {record[0]} - {record[1]} treated by Dr. {record[2]}\n  Diagnosis: {diagnosis}\n")
    
    def __del__(self):
        """Close database connection when application closes"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the Hospital Management System?"):
            app.conn.close()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
