from models.user import User

class Instructor(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.role = "Instructor"
        self.courses = []

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            return f"Course '{course.title}' added successfully!"
        return f"Course '{course.title}' already exists!"

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            return f"Course '{course.title}' removed successfully!"
        return f"Course '{course.title}' not found!"

    def get_info(self):
        return f"Instructor: {self.name} | Courses taught: {len(self.courses)}"

    def __str__(self):
        return f"[Instructor] {self.name}"