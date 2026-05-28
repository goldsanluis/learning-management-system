import json
import os

class FileManager:
    def __init__(self, filename="data/lms_data.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({
                    "courses": [],
                    "students": [],
                    "instructors": []
                }, f)

    def save_data(self, service):
        data = {
            "courses": [],
            "students": [],
            "instructors": []
        }

        for instructor in service.instructors:
            data["instructors"].append({
                "user_id": instructor.user_id,
                "name": instructor.name,
                "email": instructor.email,
                "password": instructor.password
            })

        for student in service.students:
            data["students"].append({
                "user_id": student.user_id,
                "name": student.name,
                "email": student.email,
                "password": student.password
            })

        for course in service.courses:
            data["courses"].append({
                "course_id": course.course_id,
                "title": course.title,
                "description": course.description,
                "instructor": course.instructor.name,
                "pdf_file": course.pdf_file,
                "date_created": course.date_created,
                "students": [s.name for s in course.students]
            })

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"courses": [], "students": [], "instructors": []}