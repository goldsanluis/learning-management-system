from models.user import User

class Student(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.role = "Student"
        self.enrolled_courses = []

    def enroll(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            return f"Successfully enrolled in {course.title}!"
        return f"Already enrolled in {course.title}!"

    def unenroll(self, course):
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            return f"Successfully unenrolled from {course.title}!"
        return f"Not enrolled in {course.title}!"

    def get_info(self):
        return f"Student: {self.name} | Enrolled courses: {len(self.enrolled_courses)}"

    def __str__(self):
        return f"[Student] {self.name}"