import tkinter as tk
from gui.course_form import CourseForm
from gui.enrollment_view import EnrollmentView
from services.enrollment_service import EnrollmentService
from services.pdf_service import PDFService
from file_handler.file_manager import FileManager

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Learning Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a2e")

        self.service = EnrollmentService()
        self.pdf_service = PDFService()
        self.file_manager = FileManager()

        # Add a default instructor
        self.default_instructor = self.service.add_instructor(
            "Admin Instructor", "admin@lms.com", "admin123"
        )

        self.setup_header()
        self.setup_main()

    def setup_header(self):
        header = tk.Frame(self.root, bg="#16213e", pady=10)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📚 Learning Management System",
            font=("Helvetica", 20, "bold"),
            bg="#16213e",
            fg="#e94560"
        ).pack()

    def setup_main(self):
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.course_form = CourseForm(
            main_frame,
            self.service,
            self.pdf_service,
            self.file_manager,
            self.default_instructor,
            self.refresh
        )
        self.course_form.frame.pack(side="left", fill="both", expand=True, padx=5)

        self.enrollment_view = EnrollmentView(
            main_frame,
            self.service,
            self.pdf_service,
            self.file_manager
        )
        self.enrollment_view.frame.pack(side="right", fill="both", expand=True, padx=5)

    def refresh(self):
        self.enrollment_view.refresh()

    def run(self):
        self.root.mainloop()