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
            entry = ttk.Combobox(frame, values=["Male", "Female", "Other"], font=("Arial", 14), width=width, state='readonly')
        elif label_text == "Course:":
            entry = ttk.Combobox(frame, values=["Data Science", "Machine Learning", "Artificial Intelligence"], font=("Arial", 14), width=width, state='readonly')
        elif label_text == "Candidate Phone:":
            entry = ttk.Entry(frame, font=("Arial", 14), width=width)
            entry.config(validate="key", validatecommand=(entry.register(validate_phone), "%P"))
        else:
            entry = ttk.Entry(frame, font=("Arial", 14), width=width)
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
            messagebox.showinfo("Enrollment Complete", "8 entries have been entered. Showing top 3 students with highest percentage.")
            # Show top 3 students
            show_top_students(conn)

        # Clear entry fields
        reset_entries(student_entries)

    except ValueError:
        messagebox.showerror("Error", "Invalid input for percentage.")

def reset_entries(student_entries):
    for entry in student_entries:
        entry.delete(0, "end")

def show_enrolled_students_table(conn):
    enrolled_students = conn.cursor().execute("SELECT * FROM students").fetchall()

    if not enrolled_students:
        messagebox.showinfo("Enrolled Students", "No students enrolled yet.")
        return

    # Create new window for displaying enrolled students in a table
    enrolled_students_window = Toplevel()
    enrolled_students_window.title("Enrolled Students")

    # Create Treeview widget
    tree = ttk.Treeview(enrolled_students_window, columns=('Name', 'Email', 'Phone', 'Age', 'Gender', 'DOB', 'Nationality', 'Qualification', 'Course', 'Percentage'), show='headings')
    tree.pack(fill='both', expand=True)

    # Set column headings
    for col in ('Name', 'Email', 'Phone', 'Age', 'Gender', 'DOB', 'Nationality', 'Qualification', 'Course', 'Percentage'):
        tree.heading(col, text=col)

    # Insert data into the treeview
    for student in enrolled_students:
        tree.insert('', 'end', values=student)

def show_top_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY percentage DESC LIMIT 3")
    selected_students = cursor.fetchall()

    # Display selected students
    selected_students_msg = "\n".join([f"{student[1]}: {student[10]}%" for student in selected_students])
    messagebox.showinfo("Top 3 Students", f"Top 3 students with highest percentage:\n\n{selected_students_msg}")

def main():
    root = tk.Tk()
    root.title("Course Enrollment App")
    root.state("zoomed")

    # Connect to the SQLite database
    try:
        conn = sqlite3.connect("enrollment.db")
        create_table(conn)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
        root.destroy()

    show_enrollment_frame(root, conn)
    root.mainloop()

if __name__ == "__main__":
    main()
