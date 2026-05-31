# ============================================================
# login_window.py - LoginWindow class
# Handles user login and registration for both
# Students and Instructors. First screen shown on startup.
# ============================================================

import tkinter as tk
from tkinter import messagebox
from gui.theme import *

class LoginWindow:
    def __init__(self, service, file_manager, on_login_success):
        self.service = service
        self.file_manager = file_manager
        self.on_login_success = on_login_success

        self.root = tk.Tk()
        self.root.title("LMS - Login")
        self.root.geometry("440x560")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        # ── Top Gold Banner ────────────────────────────────
        banner = tk.Frame(self.root, bg=GOLD_MEDIUM, pady=18)
        banner.pack(fill="x")

        tk.Label(
            banner,
            text="📚 Learning Management",
            font=FONT_TITLE,
            bg=GOLD_MEDIUM,
            fg=TEXT_DARK
        ).pack()

        tk.Label(
            banner,
            text="S Y S T E M",
            font=("Helvetica", 11, "bold"),
            bg=GOLD_MEDIUM,
            fg=TEXT_DARK
        ).pack()


        # ── Gold Divider ───────────────────────────────────
        tk.Frame(self.root, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        # ── Login Form ─────────────────────────────────────
        form_outer = tk.Frame(self.root, bg=BG_DARK, pady=20, padx=30)
        form_outer.pack(fill="x")

        tk.Label(
            form_outer,
            text="Welcome Back",
            font=FONT_HEADER,
            bg=BG_DARK,
            fg=GOLD_BRIGHT
        ).pack(pady=(0, 15))

        form = tk.Frame(form_outer, bg=BG_MEDIUM, padx=20, pady=20)
        form.pack(fill="x")

        # Role selector
        tk.Label(form, text="Login as:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=TEXT_WHITE).grid(row=0, column=0, sticky="w", pady=6)
        self.role_var = tk.StringVar(value="Student")
        rf = tk.Frame(form, bg=BG_MEDIUM)
        rf.grid(row=0, column=1, sticky="w")
        for role in ["Student", "Instructor"]:
            tk.Radiobutton(rf, text=role, variable=self.role_var, value=role,
                           bg=BG_MEDIUM, fg=GOLD_PALE, selectcolor=BG_LIGHT,
                           activebackground=BG_MEDIUM, activeforeground=GOLD_BRIGHT,
                           font=FONT_BODY).pack(side="left", padx=5)

        # Email
        tk.Label(form, text="Email:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=TEXT_WHITE).grid(row=1, column=0, sticky="w", pady=6)
        self.email_entry = tk.Entry(form, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
                                    insertbackground=GOLD_BRIGHT, relief="flat",
                                    bd=6, highlightthickness=1,
                                    highlightbackground=GOLD_DARK,
                                    highlightcolor=GOLD_BRIGHT)
        self.email_entry.grid(row=1, column=1, sticky="ew", pady=6)

        # Password
        tk.Label(form, text="Password:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=TEXT_WHITE).grid(row=2, column=0, sticky="w", pady=6)
        self.password_entry = tk.Entry(form, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
                                       insertbackground=GOLD_BRIGHT, relief="flat",
                                       bd=6, show="*", highlightthickness=1,
                                       highlightbackground=GOLD_DARK,
                                       highlightcolor=GOLD_BRIGHT)
        self.password_entry.grid(row=2, column=1, sticky="ew", pady=6)
        form.columnconfigure(1, weight=1)

        # Login button
        tk.Button(
            form_outer, text="Login  →",
            font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
            relief="flat", padx=10, pady=8, cursor="hand2",
            activebackground=GOLD_BRIGHT, activeforeground=TEXT_DARK,
            command=self.login
        ).pack(pady=12, fill="x")

        # Divider
        tk.Label(self.root, text="──── Don't have an account? ────",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_GRAY).pack()

        # Register button
        tk.Button(
            self.root, text="Register New Account",
            font=FONT_BODY, bg=BG_MEDIUM, fg=GOLD_PALE,
            relief="flat", padx=10, pady=7, cursor="hand2",
            activebackground=BG_LIGHT, activeforeground=GOLD_BRIGHT,
            command=self.open_register
        ).pack(pady=8, padx=30, fill="x")

        # Hint
        tk.Label(
            self.root,
            text="Default: admin@lms.com  /  admin123",
            font=FONT_SMALL, bg=BG_DARK, fg=TEXT_GRAY
        ).pack(pady=6)

        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields!", parent=self.root)
            return

        user = None
        if role == "Instructor":
            user = self.service.get_instructor_by_email(email)
        else:
            user = self.service.get_student_by_email(email)

        if not user:
            messagebox.showerror("Error", f"No {role} found with that email!", parent=self.root)
            return
        if user.password != password:
            messagebox.showerror("Error", "Incorrect password!", parent=self.root)
            return

        self.root.destroy()
        self.on_login_success(user, role)

    def open_register(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Register")
        reg_win.geometry("400x420")
        reg_win.configure(bg=BG_DARK)
        reg_win.resizable(False, False)
        reg_win.grab_set()

        tk.Frame(reg_win, bg=GOLD_MEDIUM, pady=12).pack(fill="x")
        tk.Label(reg_win, text="Create Account", font=FONT_HEADER,
                 bg=GOLD_MEDIUM, fg=TEXT_DARK).place(relx=0.5, rely=0, anchor="n", y=10)

        tk.Frame(reg_win, bg=GOLD_MEDIUM, pady=12).pack(fill="x")
        tk.Frame(reg_win, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        tk.Label(reg_win, text="Create Account", font=FONT_HEADER,
                 bg=BG_DARK, fg=GOLD_BRIGHT).pack(pady=12)

        form = tk.Frame(reg_win, bg=BG_MEDIUM, padx=20, pady=15)
        form.pack(padx=25, fill="x")

        reg_role = tk.StringVar(value="Student")
        tk.Label(form, text="Register as:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=TEXT_WHITE).grid(row=0, column=0, sticky="w", pady=5)
        rf = tk.Frame(form, bg=BG_MEDIUM)
        rf.grid(row=0, column=1, sticky="w")
        for role in ["Student", "Instructor"]:
            tk.Radiobutton(rf, text=role, variable=reg_role, value=role,
                           bg=BG_MEDIUM, fg=GOLD_PALE, selectcolor=BG_LIGHT,
                           activebackground=BG_MEDIUM, activeforeground=GOLD_BRIGHT,
                           font=FONT_BODY).pack(side="left", padx=5)

        fields = {}
        for i, label in enumerate(["Name:", "Email:", "Password:"], start=1):
            tk.Label(form, text=label, font=FONT_BODY,
                     bg=BG_MEDIUM, fg=TEXT_WHITE).grid(row=i, column=0, sticky="w", pady=5)
            e = tk.Entry(form, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
                         insertbackground=GOLD_BRIGHT, relief="flat", bd=6,
                         show="*" if label == "Password:" else "",
                         highlightthickness=1, highlightbackground=GOLD_DARK,
                         highlightcolor=GOLD_BRIGHT)
            e.grid(row=i, column=1, sticky="ew", pady=5)
            fields[label] = e
        form.columnconfigure(1, weight=1)

        def register():
            name     = fields["Name:"].get().strip()
            email    = fields["Email:"].get().strip()
            password = fields["Password:"].get().strip()
            role     = reg_role.get()
            if not all([name, email, password]):
                messagebox.showerror("Error", "Please fill in all fields!", parent=reg_win)
                return
            if self.service.get_instructor_by_email(email) or self.service.get_student_by_email(email):
                messagebox.showerror("Error", "Email already registered!", parent=reg_win)
                return
            if role == "Instructor":
                self.service.add_instructor(name, email, password)
            else:
                self.service.add_student(name, email, password)
            self.file_manager.save_data(self.service)
            messagebox.showinfo("Success", f"{role} account created! You can now log in.", parent=reg_win)
            reg_win.destroy()

        tk.Button(
            reg_win, text="✅  Create Account",
            font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
            relief="flat", padx=10, pady=8, cursor="hand2",
            activebackground=GOLD_BRIGHT,
            command=register
        ).pack(pady=15, padx=25, fill="x")

    def run(self):
        self.root.mainloop()
