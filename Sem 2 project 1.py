import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CourseEnrollmentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Course Enrollment App")
        self.master.state("zoomed")

        try:
            self.conn = sqlite3.connect("enrollment.db")
            self.create_table()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            self.master.destroy()

        self.current_frame = None
        self.student_entries = []

        self.setup_ui()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
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
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create table: {e}")

    def setup_ui(self):
        self.show_enrollment_frame()

    def show_enrollment_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack(fill="both", expand=True)

        tk.Label(self.current_frame, text="Course Enrollment", font=("Arial", 24, "bold")).pack(pady=(20, 10))

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

        for label_text, width in fields:
            frame = tk.Frame(self.current_frame)
            frame.pack(pady=10)
            tk.Label(frame, text=label_text, font=("Arial", 14)).pack(side="left", padx=(10, 5))
            if label_text == "Gender:":
                entry = ttk.Combobox(frame, values=["Male", "Female", "Other"], font=("Arial", 14), width=width)
            elif label_text == "Course:":
                entry = ttk.Combobox(frame, values=["Data Science", "Machine Learning", "Artificial Intelligence"], font=("Arial", 14), width=width)
            elif label_text == "Candidate Phone:":
                entry = tk.Entry(frame, font=("Arial", 14), width=width)
                entry.config(validate="key", validatecommand=(self.master.register(self.validate_phone), "%P"))
            else:
                entry = tk.Entry(frame, font=("Arial", 14), width=width)
            entry.pack(side="left", padx=(0, 10))
            self.student_entries.append(entry)

        tk.Button(self.current_frame, text="Enroll", command=self.enroll, font=("Arial", 14)).pack(pady=20)

        tk.Button(self.current_frame, text="Show Enrolled Students", command=self.show_enrolled_students_table, font=("Arial", 14)).pack(pady=10)

    def validate_phone(self, phone):
        return len(phone) <= 10 and (phone == "" or phone.isdigit())

    def enroll(self):
        try:
            data = [entry.get() for entry in self.student_entries]
            name, email, phone, age, gender, dob, nationality, qualification, course, percentage = data

            if not all(data):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            percentage = float(percentage)

            if percentage < 60:
                messagebox.showerror("Error", "Your percentage is less than 60. You are not eligible for this course.")
                return

            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO students (name, email, phone, age, gender, dob, nationality, qualification, course, percentage)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (name, email, phone, age, gender, dob, nationality, qualification, course, percentage))
            self.conn.commit()

            messagebox.showinfo("Enrollment Successful", "You have successfully enrolled in the course.")

            if len(cursor.execute("SELECT * FROM students").fetchall()) == 8:
                messagebox.showinfo("Enrollment Complete", "8 entries have been entered. Showing top 3 students with highest percentage.")
                self.show_top_students()

            self.reset_entries()

        except ValueError:
            messagebox.showerror("Error", "Invalid input for percentage.")

    def reset_entries(self):
        for entry in self.student_entries:
            entry.delete(0, "end")

    def show_enrolled_students_table(self):
        enrolled_students = self.conn.cursor().execute("SELECT * FROM students").fetchall()

        if not enrolled_students:
            messagebox.showinfo("Enrolled Students", "No students enrolled yet.")
            return

        enrolled_students_window = tk.Toplevel(self.master)
        enrolled_students_window.title("Enrolled Students")

        tree = ttk.Treeview(enrolled_students_window, columns=('Name', 'Email', 'Phone', 'Age', 'Gender', 'DOB', 'Nationality', 'Qualification', 'Course', 'Percentage'), show='headings')
        tree.pack(fill='both', expand=True)

        for col in ('Name', 'Email', 'Phone', 'Age', 'Gender', 'DOB', 'Nationality', 'Qualification', 'Course', 'Percentage'):
            tree.heading(col, text=col)

        for student in enrolled_students:
            tree.insert('', 'end', values=student)

    def show_top_students(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY percentage DESC LIMIT 3")
        selected_students = cursor.fetchall()

        selected_students_msg = "\n".join([f"{student[1]}: {student[10]}%" for student in selected_students])
        messagebox.showinfo("Top 3 Students", f"Top 3 students with highest percentage:\n\n{selected_students_msg}")

def main():
    root = tk.Tk()
    app = CourseEnrollmentApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
