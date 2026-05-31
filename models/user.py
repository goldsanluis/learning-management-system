# ============================================================
# user.py - Base User class
# Serves as the parent class for Student and Instructor.
# Demonstrates OOP inheritance principle.
# ============================================================

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
