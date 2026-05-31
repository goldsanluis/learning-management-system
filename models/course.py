# ============================================================
# course.py - Course class
# Represents a course in the LMS.
# Manages students enrolled and PDF attachment.
# ============================================================

from datetime import datetime

class Course:
    def __init__(self, course_id, title, description, instructor):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.instructor = instructor      # Instructor object who owns this course
        self.students = []                # List of Student objects enrolled
        self.pdf_file = None              # Path to attached PDF file
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_student(self, student):
        # Enroll a student if not already enrolled
        if student not in self.students:
            self.students.append(student)
            return f"{student.name} enrolled successfully!"
        return f"{student.name} is already enrolled!"

    def remove_student(self, student):
        # Remove a student from this course
        if student in self.students:
            self.students.remove(student)
            return f"{student.name} unenrolled successfully!"
        return f"{student.name} is not enrolled!"

    def attach_pdf(self, pdf_path):
        # Attach a PDF file path to this course
        self.pdf_file = pdf_path
        return f"PDF attached to {self.title}!"

    def __str__(self):
        return (f"Course ID: {self.course_id}\n"
                f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Instructor: {self.instructor.name}\n"
                f"Students enrolled: {len(self.students)}\n"
                f"PDF: {self.pdf_file if self.pdf_file else 'No PDF attached'}\n"
                f"Date Created: {self.date_created}")
