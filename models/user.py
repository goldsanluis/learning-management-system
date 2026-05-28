class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = "User"

    def get_info(self):
        return f"{self.role}: {self.name} ({self.email})"

    def __str__(self):
        return f"[{self.role}] {self.name}"
    