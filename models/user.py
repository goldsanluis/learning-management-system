# ============================================================
# user.py - Base User class
# Serves as the parent class for Student and Instructor.
# Demonstrates OOP inheritance principle.
# ============================================================

"""LMS Source Signature

__author__     = "Ghani Regina Gold San Luis"
__group__      = "Group 6"
__course__     = "CMPE 103 - Object Oriented Programming"
__school__     = "Polytechnic University of the Philippines"
__section__    = "BSCPE 2-0"
__github__     = "https://github.com/goldsanluis/learning-management-system"
"""



class User:
    def __init__(self, user_id, name, email, password):
        # Core attributes shared by all users
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = "User"

    def get_info(self):
        # Returns a readable summary of the user
        return f"{self.role}: {self.name} ({self.email})"

    def __str__(self):
        return f"[{self.role}] {self.name}"
