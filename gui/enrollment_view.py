import tkinter as tk
from tkinter import messagebox, filedialog
import os

class EnrollmentView:
    def __init__(self, parent, service, pdf_service, file_manager):
        self.service = service
        self.pdf_service = pdf_service
        self.file_manager = file_manager

        self.frame = tk.Frame(parent, bg="#16213e", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="Courses & Enrollment",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(pady=10)

        # Course List
        self.listbox = tk.Listbox(
            self.frame,
            font=("Helvetica", 10),
            bg="#0f3460",
            fg="white",
            selectbackground="#e94560",
            relief="flat",
            bd=5,
            height=15
        )
        self.listbox.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Student Name Entry
        tk.Label(
            self.frame,
            text="Student Name:",
            font=("Helvetica", 11),
            bg="#16213e",
            fg="white"
        ).pack(anchor="w", pady=2)

        self.student_entry = tk.Entry(
            self.frame,
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=5
        )
        self.student_entry.pack(fill="x", pady=2)

        # Enroll Button
        tk.Button(
            self.frame,
            text="Enroll Student ✅",
            font=("Helvetica", 12, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.enroll_student
        ).pack(pady=5, fill="x")

        # Unenroll Button
        tk.Button(
            self.frame,
            text="Unenroll Student ❌",
            font=("Helvetica", 12, "bold"),
            bg="#0f3460",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.unenroll_student
        ).pack(pady=5, fill="x")

        # Download PDF Button
        tk.Button(
            self.frame,
            text="Download PDF 📥",
            font=("Helvetica", 12, "bold"),
            bg="#0f3460",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.download_pdf
        ).pack(pady=5, fill="x")

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        courses = self.service.get_all_courses()
        if not courses:
            self.listbox.insert(tk.END, "No courses yet!")
            return
        for course in courses:
            self.listbox.insert(tk.END, f"─────────────────────")
            self.listbox.insert(tk.END, f"ID: {course.course_id} | {course.title}")
            self.listbox.insert(tk.END, f"👨‍🏫 {course.instructor.name}")
            self.listbox.insert(tk.END, f"📝 {course.description}")
            self.listbox.insert(tk.END, f"👥 Students: {len(course.students)}")
            self.listbox.insert(tk.END, f"📄 PDF: {'Yes ✅' if course.pdf_file else 'None ❌'}")

    def get_selected_course(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a course first!")
            return None
        selected_text = self.listbox.get(selected[0])
        if "ID:" in selected_text:
            course_id = int(selected_text.split("|")[0].replace("ID:", "").strip())
            for course in self.service.get_all_courses():
                if course.course_id == course_id:
                    return course
        return None

    def enroll_student(self):
        course = self.get_selected_course()
        if not course:
            return
        student_name = self.student_entry.get()
        if not student_name:
            messagebox.showerror("Error", "Please enter a student name!")
            return
        student = self.service.add_student(student_name, f"{student_name}@lms.com", "password123")
        result = self.service.enroll_student(student, course)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh()

    def unenroll_student(self):
        course = self.get_selected_course()
        if not course:
            return
        student_name = self.student_entry.get()
        if not student_name:
            messagebox.showerror("Error", "Please enter a student name!")
            return
        student = None
        for s in self.service.students:
            if s.name == student_name:
                student = s
                break
        if not student:
            messagebox.showerror("Error", "Student not found!")
            return
        result = self.service.unenroll_student(student, course)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh()

    def download_pdf(self):
        course = self.get_selected_course()
        if not course:
            return
        destination = filedialog.askdirectory(title="Select Download Folder")
        if not destination:
            return
        result = self.pdf_service.download_pdf(course, destination)
        messagebox.showinfo("Result", result)