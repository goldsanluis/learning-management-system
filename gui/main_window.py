# ============================================================
# main_window.py - MainWindow class
# Main application window shown after login.
# ============================================================

import tkinter as tk
from gui.course_form import CourseForm
from gui.enrollment_view import EnrollmentView
from gui.theme import *

class MainWindow:
    def __init__(self, current_user, role, service, pdf_service, file_manager):
        self.current_user = current_user
        self.role = role
        self.service = service
        self.pdf_service = pdf_service
        self.file_manager = file_manager

        self.root = tk.Tk()
        self.root.title("Learning Management System")
        self.root.geometry("1050x700")
        self.root.configure(bg=BG_DARK)

        self.setup_header()
        self.setup_main()

    def setup_header(self):
        # Gold top banner
        header = tk.Frame(self.root, bg=GOLD_MEDIUM, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📚  Learning Management System",
            font=FONT_TITLE,
            bg=GOLD_MEDIUM,
            fg=TEXT_DARK
        ).pack(side="left", padx=20)

        # Role badge on the right
        badge_color = GOLD_DARK if self.role == "Instructor" else BG_MEDIUM
        tk.Label(
            header,
            text=f"  👤 {self.current_user.name}   |   {self.role}  ",
            font=FONT_BODY,
            bg=badge_color,
            fg=GOLD_PALE,
            relief="flat", padx=8, pady=4
        ).pack(side="right", padx=20)

        # Gold line under the header
        tk.Button(
            header,
            text="🚪 Logout",
            font=FONT_BODY,
            bg=GOLD_DARK,
            fg=TEXT_WHITE,
            relief="flat",
            padx=8, pady=4,
            cursor="hand2",
            activebackground=DANGER,
            activeforeground=TEXT_WHITE,
            command=self.logout
        ).pack(side="right", padx=10)

        tk.Frame(self.root, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        stats_bar = tk.Frame(self.root, bg=BG_MEDIUM, pady=5)
        stats_bar.pack(fill="x")

        total_courses = len(self.service.get_all_courses())
        total_students = len(self.service.students)

        tk.Label(
            stats_bar,
            text=f"📚 Total Courses: {total_courses}     👥 Total Students: {total_students}     👤 Logged in as: {self.current_user.name} ({self.role})",
            font=FONT_SMALL,
            bg=BG_MEDIUM,
            fg=GOLD_PALE
        ).pack(side="left", padx=20)


    def logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            from main import main
            main()

    def setup_main(self):


        main_frame = tk.Frame(self.root, bg=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=15, pady=12)

        if self.role == "Instructor":
            self.course_form = CourseForm(
                main_frame, self.service, self.pdf_service,
                self.file_manager, self.current_user, self.refresh
            )
            self.course_form.frame.pack(side="left", fill="both", expand=True, padx=5)

        self.enrollment_view = EnrollmentView(
            main_frame, self.service, self.pdf_service,
            self.file_manager, self.current_user, self.role
        )
        self.enrollment_view.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.enrollment_view.refresh()
        if self.role == "Instructor":
            self.course_form.refresh_my_courses()

    def run(self):
        self.root.mainloop()
