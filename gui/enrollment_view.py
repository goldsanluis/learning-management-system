# ============================================================
# enrollment_view.py - EnrollmentView class
# Right panel for browsing courses, enrolling, and PDFs.
# ============================================================

import tkinter as tk
from tkinter import messagebox, filedialog
from gui.theme import *

class EnrollmentView:
    def __init__(self, parent, service, pdf_service, file_manager, current_user, role):
        self.service = service
        self.pdf_service = pdf_service
        self.file_manager = file_manager
        self.current_user = current_user
        self.role = role
        self.course_index_map = {}

        # ── Main Frame ─────────────────────────────────────
        self.frame = tk.Frame(parent, bg=BG_MEDIUM, padx=12, pady=12,
                              highlightthickness=1, highlightbackground=GOLD_DARK)

        tk.Label(self.frame, text="🎓  Courses & Enrollment",
                 font=FONT_HEADER, bg=BG_MEDIUM, fg=GOLD_BRIGHT).pack(pady=(6, 12))
        tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=(0, 8))

        # ── Course Listbox ─────────────────────────────────
        tk.Label(self.frame, text="Available Courses:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=GOLD_PALE).pack(anchor="w", pady=(0, 4))

        search_frame = tk.Frame(self.frame, bg=BG_MEDIUM)
        search_frame.pack(fill="x", pady=(0, 6))

        tk.Label(search_frame, text="🔍", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=GOLD_PALE).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_courses())

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
            insertbackground=GOLD_BRIGHT, relief="flat", bd=6,
            highlightthickness=1, highlightbackground=GOLD_DARK,
            highlightcolor=GOLD_BRIGHT
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(6, 0))

        list_frame = tk.Frame(self.frame, bg=BG_MEDIUM)
        list_frame.pack(fill="both", expand=True)


        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame, font=("Courier", 10),
            bg=BG_DARK, fg=GOLD_PALE,
            selectbackground=GOLD_DARK,
            selectforeground=TEXT_WHITE,
            relief="flat", bd=0,
            height=12,
            yscrollcommand=scroll.set
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.listbox.yview)

        tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=8)

        # ── My Enrolled Courses (Students only) ────────────
        if self.role == "Student":
            tk.Label(self.frame, text="My Enrolled Courses:", font=FONT_BODY,
                     bg=BG_MEDIUM, fg=GOLD_PALE).pack(anchor="w", pady=(0, 4))

            enrolled_frame = tk.Frame(self.frame, bg=BG_MEDIUM)
            enrolled_frame.pack(fill="x")

            enrolled_scroll = tk.Scrollbar(enrolled_frame)
            enrolled_scroll.pack(side="right", fill="y")

            self.enrolled_listbox = tk.Listbox(
                enrolled_frame, font=("Courier", 10),
                bg=BG_DARK, fg=SUCCESS,
                selectbackground=GOLD_DARK,
                relief="flat", bd=0,
                height=4,
                yscrollcommand=enrolled_scroll.set
            )
            self.enrolled_listbox.pack(side="left", fill="x", expand=True)
            enrolled_scroll.config(command=self.enrolled_listbox.yview)

            tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=8)

        # ── Action Buttons ─────────────────────────────────
        if self.role == "Student":
            tk.Button(self.frame, text="✅  Enroll in Selected Course",
                      font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
                      relief="flat", padx=10, pady=7, cursor="hand2",
                      activebackground=GOLD_BRIGHT, activeforeground=TEXT_DARK,
                      command=self.enroll_student).pack(pady=4, fill="x")

            tk.Button(self.frame, text="❌  Unenroll from Selected Course",
                      font=FONT_BUTTON, bg=BG_LIGHT, fg=GOLD_PALE,
                      relief="flat", padx=10, pady=7, cursor="hand2",
                      activebackground=GOLD_DARK, activeforeground=TEXT_WHITE,
                      command=self.unenroll_student).pack(pady=4, fill="x")

            tk.Button(self.frame, text="📥  Download Course PDF",
                      font=FONT_BUTTON, bg=BG_LIGHT, fg=GOLD_PALE,
                      relief="flat", padx=10, pady=7, cursor="hand2",
                      activebackground=GOLD_DARK, activeforeground=TEXT_WHITE,
                      command=self.download_pdf).pack(pady=4, fill="x")
        else:
            tk.Label(self.frame, text="Select a course to view details.",
                     font=FONT_SMALL, bg=BG_MEDIUM, fg=TEXT_GRAY).pack(pady=4)

        # Refresh button
        tk.Button(self.frame, text="🔄  Refresh",
                  font=FONT_SMALL, bg=BG_MEDIUM, fg=TEXT_GRAY,
                  relief="flat", cursor="hand2",
                  activebackground=BG_LIGHT, activeforeground=GOLD_PALE,
                  command=self.refresh).pack(pady=6)

        tk.Button(self.frame, text="📋  View Course Details",
              font=FONT_BUTTON, bg=BG_LIGHT, fg=GOLD_PALE,
              relief="flat", padx=10, pady=7, cursor="hand2",
              activebackground=GOLD_DARK, activeforeground=TEXT_WHITE,
              command=self.view_course_details).pack(pady=4, fill="x")

        self.refresh()

    def filter_courses(self):

        query = self.search_var.get().strip().lower()
        self.listbox.delete(0, tk.END)
        self.course_index_map = {}
        courses = self.service.get_all_courses()

        if not courses:
            self.listbox.insert(tk.END, "  No courses available yet.")
            return

        filtered = [c for c in courses if query in c.title.lower()] if query else courses

        if not filtered:
            self.listbox.insert(tk.END, "  No courses match your search.")
            return

        idx = 0
        for course in filtered:
            for _ in range(6):
                self.course_index_map[idx] = course
                idx += 1
            pdf_status = "Available ✅" if course.pdf_file else "None ❌"
            self.listbox.insert(tk.END, f"  {'─' * 38}")
            self.listbox.insert(tk.END, f"  📘 [ID:{course.course_id}]  {course.title}")
            self.listbox.insert(tk.END, f"  👨‍🏫  {course.instructor.name}")
            self.listbox.insert(tk.END, f"  📝  {course.description}")
            self.listbox.insert(tk.END, f"  👥  Enrolled: {len(course.students)} students")
            self.listbox.insert(tk.END, f"  📄  PDF: {pdf_status}")

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.course_index_map = {}
        courses = self.service.get_all_courses()


        if not courses:
            self.listbox.insert(tk.END, "  No courses available yet.")
            return

        idx = 0
        for course in courses:
            # Map every row of this course block to the same Course object
            for _ in range(6):
                self.course_index_map[idx] = course
                idx += 1

            pdf_status = "Available ✅" if course.pdf_file else "None ❌"
            self.listbox.insert(tk.END, f"  {'─' * 38}")
            self.listbox.insert(tk.END, f"  📘 [ID:{course.course_id}]  {course.title}")
            self.listbox.insert(tk.END, f"  👨‍🏫  {course.instructor.name}")
            self.listbox.insert(tk.END, f"  📝  {course.description}")
            self.listbox.insert(tk.END, f"  👥  Enrolled: {len(course.students)} students")
            self.listbox.insert(tk.END, f"  📄  PDF: {pdf_status}")

        if self.role == "Student":
            self.enrolled_listbox.delete(0, tk.END)
            enrolled = self.service.get_enrolled_courses(self.current_user)
            if not enrolled:
                self.enrolled_listbox.insert(tk.END, "  Not enrolled in any courses yet.")
            else:
                for c in enrolled:
                    self.enrolled_listbox.insert(tk.END, f"  ✅  [ID:{c.course_id}]  {c.title}")

    def get_selected_course(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a course from the list first!")
            return None
        course = self.course_index_map.get(selected[0])
        if not course:
            messagebox.showerror("Error", "Please click on a course row!")
            return None
        return course

    def enroll_student(self):
        course = self.get_selected_course()
        if not course:
            return
        result = self.service.enroll_student(self.current_user, course)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Enrollment", result)
        self.refresh()

    def unenroll_student(self):
        course = self.get_selected_course()
        if not course:
            return
        result = self.service.unenroll_student(self.current_user, course)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Unenrollment", result)
        self.refresh()

    def download_pdf(self):
        course = self.get_selected_course()
        if not course:
            return
        if self.current_user not in course.students:
            messagebox.showerror("Error", "You must be enrolled in this course to download its PDF!")
            return
        if not course.pdf_file:
            messagebox.showerror("Error", "This course has no PDF attached!")
            return
        destination = filedialog.askdirectory(title="Select Download Folder")
        if not destination:
            return
        result = self.pdf_service.download_pdf(course, destination)
        messagebox.showinfo("Download", result)

    def view_course_details(self):
        course = self.get_selected_course()
        if not course:
            return

        popup = tk.Toplevel(self.frame)
        popup.title("Course Details")
        popup.geometry("480x400")
        popup.configure(bg=BG_DARK)
        popup.resizable(False, False)
        popup.grab_set()

        # Header
        tk.Frame(popup, bg=GOLD_MEDIUM, pady=10).pack(fill="x")
        tk.Label(popup, text="📋  Course Details",
                 font=FONT_HEADER, bg=GOLD_MEDIUM, fg=TEXT_DARK
                 ).place(relx=0.5, rely=0, anchor="n", y=8)
        tk.Frame(popup, bg=GOLD_MEDIUM, pady=10).pack(fill="x")
        tk.Frame(popup, bg=GOLD_BRIGHT, height=2).pack(fill="x")

        # Details
        details_frame = tk.Frame(popup, bg=BG_DARK, padx=24, pady=16)
        details_frame.pack(fill="both", expand=True)

        pdf_status = "Available ✅" if course.pdf_file else "Not attached ❌"
        enrolled = len(course.students)

        details = [
            ("Course ID",     str(course.course_id)),
            ("Title",         course.title),
            ("Description",   course.description),
            ("Instructor",    course.instructor.name),
            ("Students",      f"{enrolled} enrolled"),
            ("PDF",           pdf_status),
            ("Date Created",  course.date_created),
        ]

        for label, value in details:
            row = tk.Frame(details_frame, bg=BG_DARK)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label}:", font=FONT_BODY,
                     bg=BG_DARK, fg=GOLD_PALE, width=14,
                     anchor="w").pack(side="left")
            tk.Label(row, text=value, font=FONT_BODY,
                     bg=BG_DARK, fg=TEXT_WHITE,
                     anchor="w", wraplength=280,
                     justify="left").pack(side="left", fill="x", expand=True)

        tk.Button(popup, text="Close",
                  font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
                  relief="flat", padx=10, pady=6, cursor="hand2",
                  activebackground=GOLD_BRIGHT,
                  command=popup.destroy).pack(pady=12)

