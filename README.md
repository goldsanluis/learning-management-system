# 📚 Learning Management System

A Python-based Learning Management System built with Object-Oriented Programming principles, file handling for data persistence, PDF management, and a Tkinter GUI.

---

## 📋 Features

- **Course Management** — Add, edit, and delete courses
- **Student Enrollment** — Enroll and unenroll students from courses
- **PDF Uploads** — Attach PDF lecture files to courses
- **PDF Downloads** — Download course PDFs to your local folder
- **Instructor Support** — Courses are managed under an assigned instructor
- **Data Persistence** — All data saved to a JSON file

---

## 👥 User Roles

| Role | Permissions |
|------|-------------|
| 👨‍🏫 Instructor | Add, edit, delete courses; upload PDFs |
| 🎓 Student | Enroll/unenroll in courses; download PDFs |

---

## 🏗️ Project Structure

```
learning-management-system/
│
├── main.py                          # Entry point
├── models/
│   ├── user.py                      # Base User class
│   ├── student.py                   # Student subclass
│   ├── instructor.py                # Instructor subclass
│   └── course.py                    # Course class
├── services/
│   ├── enrollment_service.py        # Enrollment operations
│   └── pdf_service.py               # PDF upload/download
├── file_handler/
│   └── file_manager.py              # Save/load JSON
├── gui/
│   ├── main_window.py               # Main app window
│   ├── course_form.py               # Add/Edit/Delete course form
│   └── enrollment_view.py           # Course list and enrollment
└── data/
    ├── lms_data.json                 # Saved LMS data
    └── pdfs/                         # Uploaded PDF files
```

---

## 🧱 OOP Concepts Used

- **Inheritance** — Student and Instructor inherit from the base User class
- **Polymorphism** — Each user role overrides `get_info()` differently
- **Encapsulation** — All enrollment logic is inside EnrollmentService

---

## 🚀 How to Run

1. Clone the repository:
   ```
   git clone https://github.com/goldsanluis/learning-management-system.git
   ```

2. Navigate to the project folder:
   ```
   cd learning-management-system
   ```

3. Run the app:
   ```
   python main.py
   ```

---

## 🛠️ Built With

- Python 3.x
- Tkinter (GUI)
- JSON (Data persistence)
- shutil / os (PDF file handling)

---

## 👩‍💻 Developer

- **Group 6**
- Course: Object-Oriented Programming
