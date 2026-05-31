# ============================================================
# course_form.py - CourseForm class
# Panel for instructors to add, edit, and delete courses.
# ============================================================

"""LMS Source Signature

__author__     = "Ghani Regina Gold San Luis"
__group__      = "Group 6"
__course__     = "CMPE 103 - Object Oriented Programming"
__school__     = "Polytechnic University of the Philippines"
__section__    = "BSCPE 2-0"
__github__     = "https://github.com/goldsanluis/learning-management-system"
"""




import tkinter as tk
from tkinter import messagebox, filedialog
from gui.theme import *

class CourseForm:
    def __init__(self, parent, service, pdf_service, file_manager, instructor, refresh_callback):
        self.service = service
        self.pdf_service = pdf_service
        self.file_manager = file_manager
        self.instructor = instructor
        self.refresh_callback = refresh_callback
        self.selected_pdf = None

        # ── Main Frame ─────────────────────────────────────
        self.frame = tk.Frame(parent, bg=BG_MEDIUM, padx=12, pady=12,
                              highlightthickness=1, highlightbackground=GOLD_DARK)

        # Section title
        tk.Label(self.frame, text="⚙  Manage Courses",
                 font=FONT_HEADER, bg=BG_MEDIUM, fg=GOLD_BRIGHT).pack(pady=(6, 12))
        tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=(0, 10))

        # ── Input Fields ───────────────────────────────────
        self.create_label("Course Title:")
        self.title_entry = self.create_entry()

        self.create_label("Description:")
        self.desc_entry = self.create_entry()

        # PDF row
        self.create_label("Course PDF (optional):")
        pdf_frame = tk.Frame(self.frame, bg=BG_MEDIUM)
        pdf_frame.pack(fill="x", pady=2)

        self.pdf_label = tk.Label(pdf_frame, text="No PDF selected",
                                  font=FONT_SMALL, bg=BG_MEDIUM, fg=TEXT_GRAY)
        self.pdf_label.pack(side="left")

        tk.Button(pdf_frame, text="Browse 📂", font=FONT_SMALL,
                  bg=BG_LIGHT, fg=GOLD_PALE, relief="flat", cursor="hand2",
                  activebackground=GOLD_DARK, activeforeground=TEXT_WHITE,
                  command=self.browse_pdf).pack(side="right")

        # Course ID field
        self.create_label("Course ID (for edit/delete):")
        self.course_id_entry = self.create_entry()

        tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=10)

        # ── Action Buttons ─────────────────────────────────
        tk.Button(self.frame, text="➕  Add Course",
                  font=FONT_BUTTON, bg=GOLD_MEDIUM, fg=TEXT_DARK,
                  relief="flat", padx=10, pady=7, cursor="hand2",
                  activebackground=GOLD_BRIGHT, activeforeground=TEXT_DARK,
                  command=self.add_course).pack(pady=4, fill="x")

        tk.Button(self.frame, text="✏️  Edit Course",
                  font=FONT_BUTTON, bg=BG_LIGHT, fg=GOLD_PALE,
                  relief="flat", padx=10, pady=7, cursor="hand2",
                  activebackground=GOLD_DARK, activeforeground=TEXT_WHITE,
                  command=self.edit_course).pack(pady=4, fill="x")

        tk.Button(self.frame, text="🗑️  Delete Course",
                  font=FONT_BUTTON, bg=DANGER, fg=TEXT_WHITE,
                  relief="flat", padx=10, pady=7, cursor="hand2",
                  activebackground="#922B21", activeforeground=TEXT_WHITE,
                  command=self.delete_course).pack(pady=4, fill="x")

        # ── My Courses List ────────────────────────────────
        tk.Frame(self.frame, bg=GOLD_DARK, height=1).pack(fill="x", pady=10)
        tk.Label(self.frame, text="My Courses:", font=FONT_BODY,
                 bg=BG_MEDIUM, fg=GOLD_PALE).pack(anchor="w", pady=(0, 4))

        list_frame = tk.Frame(self.frame, bg=BG_MEDIUM)
        list_frame.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side="right", fill="y")

        self.my_courses_listbox = tk.Listbox(
            list_frame, font=("Courier", 10),
            bg=BG_DARK, fg=GOLD_PALE,
            selectbackground=GOLD_DARK,
            selectforeground=TEXT_WHITE,
            relief="flat", bd=0,
            yscrollcommand=scroll.set
        )
        self.my_courses_listbox.pack(fill="both", expand=True)
        scroll.config(command=self.my_courses_listbox.yview)

        self.refresh_my_courses()

    def create_label(self, text):
        tk.Label(self.frame, text=text, font=FONT_BODY,
                 bg=BG_MEDIUM, fg=TEXT_WHITE).pack(anchor="w", pady=(6, 1))

    def create_entry(self):
        e = tk.Entry(self.frame, font=FONT_BODY, bg=BG_LIGHT, fg=TEXT_WHITE,
                     insertbackground=GOLD_BRIGHT, relief="flat", bd=6,
                     highlightthickness=1, highlightbackground=GOLD_DARK,
                     highlightcolor=GOLD_BRIGHT)
        e.pack(fill="x", pady=2)
        return e

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.selected_pdf = file_path
            self.pdf_label.config(text=file_path.split("/")[-1].split("\\")[-1], fg=GOLD_PALE)

    def add_course(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        if not title or not description:
            messagebox.showerror("Error", "Please fill in Title and Description!")
            return
        course = self.service.add_course(title, description, self.instructor)
        if self.selected_pdf:
            result = self.pdf_service.upload_pdf(course, self.selected_pdf)
            messagebox.showinfo("PDF Upload", result)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Success", f"Course '{title}' added successfully!")
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.pdf_label.config(text="No PDF selected", fg=TEXT_GRAY)
        self.selected_pdf = None
        self.refresh_my_courses()
        self.refresh_callback()

    def edit_course(self):
        try:
            course_id = int(self.course_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Course ID!")
            return
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        if not title and not description:
            messagebox.showerror("Error", "Enter a new title or description to update!")
            return
        result = self.service.edit_course(course_id, title or None, description or None)
        if self.selected_pdf:
            course = self.service.get_course_by_id(course_id)
            if course:
                messagebox.showinfo("PDF", self.pdf_service.upload_pdf(course, self.selected_pdf))
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh_my_courses()
        self.refresh_callback()

    def delete_course(self):
        try:
            course_id = int(self.course_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Course ID!")
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            return
        result = self.service.delete_course(course_id)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh_my_courses()
        self.refresh_callback()

    def refresh_my_courses(self):
        self.my_courses_listbox.delete(0, tk.END)
        if not self.instructor.courses:
            self.my_courses_listbox.insert(tk.END, "  No courses yet.")
            return
        for course in self.instructor.courses:
            pdf = "📄" if course.pdf_file else "  "
            self.my_courses_listbox.insert(
                tk.END,
                f"  [ID:{course.course_id}]  {course.title}  {pdf}  👥{len(course.students)}"
            )
