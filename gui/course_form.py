import tkinter as tk
from tkinter import messagebox, filedialog

class CourseForm:
    def __init__(self, parent, service, pdf_service, file_manager, instructor, refresh_callback):
        self.service = service
        self.pdf_service = pdf_service
        self.file_manager = file_manager
        self.instructor = instructor
        self.refresh_callback = refresh_callback
        self.selected_pdf = None

        self.frame = tk.Frame(parent, bg="#16213e", padx=10, pady=10)

        tk.Label(
            self.frame,
            text="Manage Courses",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack(pady=10)

        # Course Title
        self.create_label("Course Title:")
        self.title_entry = self.create_entry()

        # Course Description
        self.create_label("Description:")
        self.desc_entry = self.create_entry()

        # PDF Upload
        self.create_label("Course PDF:")
        pdf_frame = tk.Frame(self.frame, bg="#16213e")
        pdf_frame.pack(fill="x", pady=2)

        self.pdf_label = tk.Label(
            pdf_frame,
            text="No PDF selected",
            font=("Helvetica", 10),
            bg="#16213e",
            fg="gray"
        )
        self.pdf_label.pack(side="left")

        tk.Button(
            pdf_frame,
            text="Browse 📂",
            font=("Helvetica", 10),
            bg="#0f3460",
            fg="white",
            relief="flat",
            command=self.browse_pdf
        ).pack(side="right")

        # Add Course Button
        tk.Button(
            self.frame,
            text="Add Course ➕",
            font=("Helvetica", 12, "bold"),
            bg="#e94560",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.add_course
        ).pack(pady=5, fill="x")

        # Edit Course Button
        tk.Button(
            self.frame,
            text="Edit Course ✏️",
            font=("Helvetica", 12, "bold"),
            bg="#0f3460",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.edit_course
        ).pack(pady=5, fill="x")

        # Delete Course Button
        tk.Button(
            self.frame,
            text="Delete Course 🗑️",
            font=("Helvetica", 12, "bold"),
            bg="#0f3460",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.delete_course
        ).pack(pady=5, fill="x")

        # Course ID for edit/delete
        self.create_label("Course ID (for edit/delete):")
        self.course_id_entry = self.create_entry()

    def create_label(self, text):
        tk.Label(
            self.frame,
            text=text,
            font=("Helvetica", 11),
            bg="#16213e",
            fg="white"
        ).pack(anchor="w", pady=2)

    def create_entry(self):
        entry = tk.Entry(
            self.frame,
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=5
        )
        entry.pack(fill="x", pady=2)
        return entry

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.selected_pdf = file_path
            self.pdf_label.config(text=file_path.split("/")[-1], fg="white")

    def add_course(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()

        if not all([title, description]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        course = self.service.add_course(title, description, self.instructor)

        if self.selected_pdf:
            result = self.pdf_service.upload_pdf(course, self.selected_pdf)
            messagebox.showinfo("PDF", result)

        self.file_manager.save_data(self.service)
        messagebox.showinfo("Success", f"Course '{title}' added successfully!")

        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.pdf_label.config(text="No PDF selected", fg="gray")
        self.selected_pdf = None
        self.refresh_callback()

    def edit_course(self):
        try:
            course_id = int(self.course_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Course ID!")
            return

        title = self.title_entry.get()
        description = self.desc_entry.get()
        result = self.service.edit_course(course_id, title, description)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh_callback()

    def delete_course(self):
        try:
            course_id = int(self.course_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Course ID!")
            return

        result = self.service.delete_course(course_id)
        self.file_manager.save_data(self.service)
        messagebox.showinfo("Result", result)
        self.refresh_callback()