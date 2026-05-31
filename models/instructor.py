# ============================================================
# instructor.py - Instructor class
# Inherits from User. Represents an instructor in the LMS.
# Manages courses created by the instructor.
# ============================================================

from models.user import User

class Instructor(User):
    def __init__(self, user_id, name, email, password):
        # Call parent constructor to set shared attributes
        super().__init__(user_id, name, email, password)
        self.role = "Instructor"
        self.courses = []  # List of Course objects this instructor owns

    def add_course(self, course):
        # Add a course to this instructor's list
        if course not in self.courses:
            self.courses.append(course)
            return f"Course '{course.title}' added successfully!"
        return f"Course '{course.title}' already exists!"

    def remove_course(self, course):
        # Remove a course from this instructor's list
        if course in self.courses:
            self.courses.remove(course)
            return f"Course '{course.title}' removed successfully!"
        return f"Course '{course.title}' not found!"

    def get_info(self):
        # Returns instructor summary with course count
        return f"Instructor: {self.name} | Courses taught: {len(self.courses)}"

    def __str__(self):
        return f"[Instructor] {self.name}"
