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
            text="🔑 Password",
            font=FONT_BODY,
            bg=BG_MEDIUM,
            fg=GOLD_PALE,
            relief="flat",
            padx=8, pady=4,
            cursor="hand2",
            activebackground=GOLD_DARK,
            activeforeground=TEXT_WHITE,
            command=self.change_password
        ).pack(side="right", padx=4)

        tk.Button(
            header,
            text="👤 Profile",
            font=FONT_BODY,
            bg=BG_MEDIUM,
            fg=GOLD_PALE,
            relief="flat",
            padx=8, pady=4,
            cursor="hand2",
            activebackground=GOLD_DARK,
            activeforeground=TEXT_WHITE,
            command=self.show_profile
        ).pack(side="right", padx=4)

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

    def change_password(self):
        from tkinter import messagebox
        popup = tk.Toplevel(self.root)
        popup.title("Change Password")
        popup.geometry("380x300")
        popup.configure(bg=BG_DARK)
        popup.resizable(False, False)
        popup.grab_set()

        header = tk.Frame(popup, bg=GOLD_MEDIUM, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🔑  Change Password",
                 font=FONT_HEADER, bg=GOLD_MEDIUM,
                 fg=TEXT_DARK).pack()
        tk.Frame(popup, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        form = tk.Frame(popup, bg=BG_DARK, padx=24, pady=20)
        form.pack(fill="both", expand=True)

        fields = {}
        for label in ["Current Password:", "New Password:", "Confirm New Password:"]:
            tk.Label(form, text=label, font=FONT_BODY,
                     bg=BG_DARK, fg=GOLD_PALE).pack(anchor="w", pady=(6,1))
            e = tk.Entry(form, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
                         insertbackground=GOLD_BRIGHT, relief="flat",
                         bd=6, show="*", highlightthickness=1,
                         highlightbackground=GOLD_DARK,
                         highlightcolor=GOLD_BRIGHT)
            e.pack(fill="x", pady=2)
            fields[label] = e

        def save_password():
            current  = fields["Current Password:"].get().strip()
            new_pass = fields["New Password:"].get().strip()
            confirm  = fields["Confirm New Password:"].get().strip()

            if not all([current, new_pass, confirm]):
                messagebox.showerror("Error", "Please fill in all fields!", parent=popup)
                return
            if current != self.current_user.password:
                messagebox.showerror("Error", "Current password is incorrect!", parent=popup)
                return
            if new_pass != confirm:
                messagebox.showerror("Error", "New passwords do not match!", parent=popup)
                return
            if len(new_pass) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters!", parent=popup)
                return

            self.current_user.password = new_pass
            self.file_manager.save_data(self.service)
            messagebox.showinfo("Success", "Password changed successfully!", parent=popup)
            popup.destroy()

        tk.Button(popup, text="💾  Save Password",
                  font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
                  relief="flat", padx=10, pady=6, cursor="hand2",
                  activebackground=GOLD_BRIGHT,
                  command=save_password).pack(pady=10, padx=24, fill="x")

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

    def show_profile(self):
        from tkinter import messagebox
        popup = tk.Toplevel(self.root)
        popup.title("My Profile")
        popup.geometry("400x320")
        popup.configure(bg=BG_DARK)
        popup.resizable(False, False)
        popup.grab_set()

        # Header
        header = tk.Frame(popup, bg=GOLD_MEDIUM, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="👤  My Profile",
                 font=FONT_HEADER, bg=GOLD_MEDIUM,
                 fg=TEXT_DARK).pack()
        tk.Frame(popup, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        # Details
        details_frame = tk.Frame(popup, bg=BG_DARK, padx=24, pady=20)
        details_frame.pack(fill="both", expand=True)

        if self.role == "Student":
            extra_label = "Enrolled Courses"
            extra_value = str(len(self.current_user.enrolled_courses))
        else:
            extra_label = "Courses Taught"
            extra_value = str(len(self.current_user.courses))

        details = [
            ("Name",      self.current_user.name),
            ("Email",     self.current_user.email),
            ("Role",      self.role),
            ("User ID",   str(self.current_user.user_id)),
            (extra_label, extra_value),
        ]

        for label, value in details:
            row = tk.Frame(details_frame, bg=BG_DARK)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"{label}:", font=FONT_BODY,
                     bg=BG_DARK, fg=GOLD_PALE,
                     width=16, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=FONT_BODY,
                     bg=BG_DARK, fg=TEXT_WHITE,
                     anchor="w").pack(side="left")

        tk.Button(popup, text="Close",
                  font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
                  relief="flat", padx=10, pady=6, cursor="hand2",
                  activebackground=GOLD_BRIGHT,
                  command=popup.destroy).pack(pady=12)

    def run(self):
        self.root.mainloop()

