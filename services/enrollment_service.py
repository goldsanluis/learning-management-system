from models.course import Course
from models.student import Student
from models.instructor import Instructor

class EnrollmentService:
    def __init__(self):
        self.courses = []
        self.students = []
        self.instructors = []
        self.next_course_id = 1
        self.next_user_id = 1

    def add_instructor(self, name, email, password):
        instructor = Instructor(self.next_user_id, name, email, password)
        self.instructors.append(instructor)
        self.next_user_id += 1
        return instructor

    def add_student(self, name, email, password):
        student = Student(self.next_user_id, name, email, password)
        self.students.append(student)
        self.next_user_id += 1
        return student

    def add_course(self, title, description, instructor):
        course = Course(self.next_course_id, title, description, instructor)
        self.courses.append(course)
        instructor.add_course(course)
        self.next_course_id += 1
        return course

    def edit_course(self, course_id, title=None, description=None):
        for course in self.courses:
            if course.course_id == course_id:
                if title:
                    course.title = title
                if description:
                    course.description = description
                return f"Course updated successfully!"
        return "Course not found!"

    def delete_course(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                self.courses.remove(course)
                return f"Course '{course.title}' deleted successfully!"
        return "Course not found!"

    def enroll_student(self, student, course):
        result = course.add_student(student)
        student.enroll(course)
        return result

    def unenroll_student(self, student, course):
        result = course.remove_student(student)
        student.unenroll(course)
        return result

    def get_all_courses(self):
        return self.courses

    def get_enrolled_courses(self, student):
        return student.enrolled_courses