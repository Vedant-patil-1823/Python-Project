import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import Toplevel

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT,
                            phone TEXT,
                            age INTEGER,
                            gender TEXT,
                            dob TEXT,
                            nationality TEXT,
                            qualification TEXT,
                            course TEXT,
                            percentage REAL
                        )''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to create table: {e}")

def show_enrollment_frame(master, conn):
    current_frame = tk.Frame(master)
    current_frame.pack(fill="both", expand=True)

    # Title label
    tk.Label(current_frame, text="Course Enrollment", font=("Arial", 24, "bold")).pack(pady=(20, 10))

    # Input fields
    fields = [
        ("Candidate Name:", 30),
        ("Candidate Email:", 30),
        ("Candidate Phone:", 30),
        ("Age:", 10),
        ("Gender:", 15),
        ("Date of Birth:", 15),
        ("Nationality:", 30),
        ("Qualification:", 30),
        ("Course:", 27),
        ("Percentage:", 10)
    ]

    student_entries = []

    for label_text, width in fields:
        frame = tk.Frame(current_frame)
        frame.pack(pady=10)
        tk.Label(frame, text=label_text, font=("Arial", 14)).pack(side="left", padx=(10, 5))
        if label_text == "Gender:":
            entry = ttk.Combobox(frame, values=["Male", "Female", "Other"], font=("Arial", 14), width=width)
        elif label_text == "Course:":
            entry = ttk.Combobox(frame, values=["Data Science", "Machine Learning", "Artificial Intelligence"], font=("Arial", 14), width=width)
        elif label_text == "Candidate Phone:":
            entry = tk.Entry(frame, font=("Arial", 14), width=width)
            entry.config(validate="key", validatecommand=(entry.register(validate_phone), "%P"))
        else:
            entry = tk.Entry(frame, font=("Arial", 14), width=width)
        entry.pack(side="left", padx=(0, 10))
        student_entries.append(entry)

    # Submit button
    submit_button = tk.Button(current_frame, text="Enroll", command=lambda: enroll(conn, student_entries), font=("Arial", 14))
    submit_button.pack(pady=20)

def validate_phone(value):
    # Check if value is empty or contains only digits and has at most 10 characters
    return value.isdigit() and len(value) <= 10 or value == ""

def enroll(conn, student_entries):
    try:
        data = [entry.get() for entry in student_entries]
        name, email, phone, age, gender, dob, nationality, qualification, course, percentage = data

        # Validate input
        if not all(data):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Convert percentage to float
        percentage = float(percentage)

        # Check eligibility
        if percentage < 60:
            messagebox.showerror("Error", "Your percentage is less than 60. You are not eligible for this course.")
            return

        # Insert student information into the database
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO students (name, email, phone, age, gender, dob, nationality, qualification, course, percentage)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (name, email, phone, age, gender, dob, nationality, qualification, course, percentage))
        conn.commit()

        # Show enrollment success message
        messagebox.showinfo("Enrollment Successful", "You have successfully enrolled in the course.")

        # Show message box if 8 entries have been entered
        if len(cursor.execute("SELECT * FROM students").fetchall()) == 8:
            messagebox.showinfo("Enrollment Complete"), 
