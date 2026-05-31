# ============================================================
# student.py - Student class
# Inherits from User. Represents a student in the LMS.
# Manages course enrollments for a student.
# ============================================================

from models.user import User

class Student(User):
    def __init__(self, user_id, name, email, password):
        # Call parent constructor to set shared attributes
        super().__init__(user_id, name, email, password)
        self.role = "Student"
        self.enrolled_courses = []  # List of Course objects the student is enrolled in

    def enroll(self, course):
        # Add course to student's enrolled list if not already there
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            return f"Successfully enrolled in {course.title}!"
        return f"Already enrolled in {course.title}!"

    def unenroll(self, course):
        # Remove course from student's enrolled list
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            return f"Successfully unenrolled from {course.title}!"
        return f"Not enrolled in {course.title}!"

    def get_info(self):
        # Returns student summary with enrollment count
        return f"Student: {self.name} | Enrolled courses: {len(self.enrolled_courses)}"

    def __str__(self):
        return f"[Student] {self.name}"
