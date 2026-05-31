# ============================================================
# enrollment_service.py - EnrollmentService class
# Central service that manages all courses, students,
# and instructors. Acts as the main backend logic layer.
# ============================================================

from models.course import Course
from models.student import Student
from models.instructor import Instructor

class EnrollmentService:
    def __init__(self):
        self.courses = []         # All courses in the system
        self.students = []        # All registered students
        self.instructors = []     # All registered instructors
        self.next_course_id = 1   # Auto-incrementing course ID
        self.next_user_id = 1     # Auto-incrementing user ID

    # ── Instructor Management ──────────────────────────────

    def add_instructor(self, name, email, password):
        # Create and register a new instructor
        instructor = Instructor(self.next_user_id, name, email, password)
        self.instructors.append(instructor)
        self.next_user_id += 1
        return instructor

    def get_instructor_by_email(self, email):
        # Find an instructor by their email address
        for instructor in self.instructors:
            if instructor.email == email:
                return instructor
        return None

    # ── Student Management ─────────────────────────────────

    def add_student(self, name, email, password):
        # Create and register a new student
        student = Student(self.next_user_id, name, email, password)
        self.students.append(student)
        self.next_user_id += 1
        return student

    def get_student_by_email(self, email):
        # Find a student by their email address
        for student in self.students:
            if student.email == email:
                return student
        return None

    def get_student_by_name(self, name):
        # Find a student by their name
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    # ── Course Management ──────────────────────────────────

    def add_course(self, title, description, instructor):
        # Create a new course and assign it to the instructor
        course = Course(self.next_course_id, title, description, instructor)
        self.courses.append(course)
        instructor.add_course(course)
        self.next_course_id += 1
        return course

    def edit_course(self, course_id, title=None, description=None):
        # Update a course's title and/or description
        for course in self.courses:
            if course.course_id == course_id:
                if title:
                    course.title = title
                if description:
                    course.description = description
                return "Course updated successfully!"
        return "Course not found!"

    def delete_course(self, course_id):
        # Remove a course from the system by ID
        for course in self.courses:
            if course.course_id == course_id:
                # Also remove from instructor's list
                course.instructor.remove_course(course)
                self.courses.remove(course)
                return f"Course '{course.title}' deleted successfully!"
        return "Course not found!"

    def get_course_by_id(self, course_id):
        # Find a course by its ID
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    # ── Enrollment Management ──────────────────────────────

    def enroll_student(self, student, course):
        # Enroll a student in a course (updates both sides)
        result = course.add_student(student)
        student.enroll(course)
        return result

    def unenroll_student(self, student, course):
        # Remove a student from a course (updates both sides)
        result = course.remove_student(student)
        student.unenroll(course)
        return result

    def get_all_courses(self):
        # Return the full list of courses
        return self.courses

    def get_enrolled_courses(self, student):
        # Return all courses a student is enrolled in
        return student.enrolled_courses
