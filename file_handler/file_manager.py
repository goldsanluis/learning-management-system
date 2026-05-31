# ============================================================
# file_manager.py - FileManager class
# Handles saving and loading all LMS data to/from a JSON file.
# Ensures data persists between app sessions.
# ============================================================

"""LMS Source Signature

__author__     = "Ghani Regina Gold San Luis"
__group__      = "Group 6"
__course__     = "CMPE 103 - Object Oriented Programming"
__school__     = "Polytechnic University of the Philippines"
__section__    = "BSCPE 2-0"
__github__     = "https://github.com/goldsanluis/learning-management-system"
"""



import json
import os

class FileManager:
    def __init__(self, filename="data/lms_data.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # Create the data folder and empty JSON file if they don't exist
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({
                    "courses": [],
                    "students": [],
                    "instructors": [],
                    "next_course_id": 1,
                    "next_user_id": 1
                }, f, indent=4)

    def save_data(self, service):
        # Serialize all instructors, students, and courses to JSON
        data = {
            "next_course_id": service.next_course_id,
            "next_user_id": service.next_user_id,
            "instructors": [],
            "students": [],
            "courses": []
        }

        data["_meta"] = {
            "author": "Ghani Regina Gold San Luis",
            "group": "Group 6",
            "course": "CMPE 103 - Object Oriented Programming",
            "school": "Polytechnic University of the Philippines",
            "github": "https://github.com/goldsanluis/learning-management-system",
        }



        # Save instructors
        for instructor in service.instructors:
            data["instructors"].append({
                "user_id": instructor.user_id,
                "name": instructor.name,
                "email": instructor.email,
                "password": instructor.password
            })

        # Save students with their enrolled course IDs
        for student in service.students:
            data["students"].append({
                "user_id": student.user_id,
                "name": student.name,
                "email": student.email,
                "password": student.password,
                "enrolled_course_ids": [c.course_id for c in student.enrolled_courses]
            })

        # Save courses with enrolled student IDs
        for course in service.courses:
            data["courses"].append({
                "course_id": course.course_id,
                "title": course.title,
                "description": course.description,
                "instructor_id": course.instructor.user_id,
                "pdf_file": course.pdf_file,
                "date_created": course.date_created,
                "student_ids": [s.user_id for s in course.students]
            })

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self, service):
        # Load all saved data back into the service
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is missing or corrupt, start fresh
            return

        # Restore ID counters
        service.next_course_id = data.get("next_course_id", 1)
        service.next_user_id = data.get("next_user_id", 1)

        # Restore instructors
        for i_data in data.get("instructors", []):
            from models.instructor import Instructor
            instructor = Instructor(
                i_data["user_id"],
                i_data["name"],
                i_data["email"],
                i_data["password"]
            )
            service.instructors.append(instructor)

        # Restore students (without enrollments for now)
        for s_data in data.get("students", []):
            from models.student import Student
            student = Student(
                s_data["user_id"],
                s_data["name"],
                s_data["email"],
                s_data["password"]
            )
            service.students.append(student)

        # Restore courses and link to instructors
        for c_data in data.get("courses", []):
            from models.course import Course

            # Find the instructor object by ID
            instructor = None
            for i in service.instructors:
                if i.user_id == c_data["instructor_id"]:
                    instructor = i
                    break

            if not instructor:
                continue  # Skip if instructor not found

            course = Course(
                c_data["course_id"],
                c_data["title"],
                c_data["description"],
                instructor
            )
            course.pdf_file = c_data.get("pdf_file")
            course.date_created = c_data.get("date_created", course.date_created)

            # Link enrolled students to the course
            for student_id in c_data.get("student_ids", []):
                for student in service.students:
                    if student.user_id == student_id:
                        course.students.append(student)
                        student.enrolled_courses.append(course)
                        break

            service.courses.append(course)
            instructor.courses.append(course)
