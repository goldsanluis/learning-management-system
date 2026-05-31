# 📚 PUP Learning Management System

A Python-based Learning Management System (LMS) built for the **Polytechnic University of the Philippines (PUP)** as a final project for Object-Oriented Programming. The system features a full Tkinter GUI, role-based access, PDF management, real-time course search, and persistent JSON data storage.

---

## 🖼️ Preview

| Login Screen | Instructor Dashboard | Student Dashboard |
|---|---|---|
| Login with email & password | Manage and create courses | Browse and enroll in courses |

---

## ✨ Features

### 🔐 Authentication
- Login and Registration for both **Students** and **Instructors**
- Secure password validation
- Default admin account: `admin@lms.com` / `admin123`

### 👨‍🏫 Instructor Features
- ➕ Add, ✏️ Edit, and 🗑️ Delete courses
- 📄 Upload PDF lecture materials to courses
- 👥 View the list of students enrolled per course
- 📊 See live stats (total courses, total students)

### 🎓 Student Features
- ✅ Enroll and ❌ Unenroll from courses
- 📥 Download course PDF materials
- 🔍 Real-time search/filter courses by name
- 📋 View full course details in a popup

### 👤 All Users
- 👤 View personal profile (name, email, role, enrolled/taught courses)
- 🔑 Change password with validation
- 🚪 Logout and return to login screen
- 📊 Stats bar showing system-wide totals

### 🏫 Pre-loaded PUP Courses
Over **60 official PUP degree programs** are pre-seeded on first launch, covering all colleges:
- College of Computer and Information Sciences (CCIS)
- College of Engineering (CE)
- College of Business Administration (CBA)
- College of Accountancy and Finance (CAF)
- College of Education (COED)
- College of Science (CS)
- College of Arts and Letters (CAL)
- College of Communication (COC)
- College of Architecture, Design and the Built Environment (CADBE)
- College of Social Sciences and Development (CSSD)
- College of Political Science and Public Administration (CPSPA)
- College of Tourism, Hospitality and Transportation Management (CTHTM)
- College of Human Kinetics (CHK)
- College of Law (CL)
- Graduate School (MBA, MSIT, MPA, and more)

---

## 👥 User Roles

| Role | Permissions |
|------|-------------|
| 👨‍🏫 **Instructor** | Add / Edit / Delete courses, Upload PDFs, View enrolled students |
| 🎓 **Student** | Browse courses, Enroll / Unenroll, Download PDFs, Search courses |

---

## 🏗️ Project Structure

```
Learning Management System/
│
├── main.py                        # App entry point + PUP course seeding
│
├── models/
│   ├── user.py                    # Base User class (OOP inheritance)
│   ├── student.py                 # Student subclass
│   ├── instructor.py              # Instructor subclass
│   └── course.py                  # Course class
│
├── services/
│   ├── enrollment_service.py      # Core business logic
│   └── pdf_service.py             # Cross-platform PDF handling
│
├── file_handler/
│   └── file_manager.py            # Save/load data to JSON
│
├── gui/
│   ├── theme.py                   # Colors, fonts, UI constants
│   ├── login_window.py            # Login & Registration screen
│   ├── main_window.py             # Main app window + header buttons
│   ├── course_form.py             # Instructor course management panel
│   └── enrollment_view.py         # Course list, search, enrollment panel
│
└── data/
    ├── lms_data.json              # Persisted LMS data
    └── pdfs/                      # Uploaded PDF files
```

---

## 🧱 OOP Concepts Demonstrated

| Concept | Where It's Used |
|---------|----------------|
| **Inheritance** | `Student` and `Instructor` both inherit from `User` |
| **Polymorphism** | Each role overrides `get_info()` differently |
| **Encapsulation** | All business logic is inside service classes |
| **Abstraction** | GUI layer is fully separated from data/service layer |
| **Custom Exceptions** | Handled via try-except throughout the app |

---

## 🚀 How to Run

### Requirements
- Python 3.x
- Tkinter (usually bundled with Python)

> **Windows:** Tkinter comes with Python. If missing, reinstall Python from [python.org](https://python.org) and check "tcl/tk and IDLE".  
> **Linux:** `sudo apt install python3-tk`  
> **Mac:** `brew install python-tk`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/goldsanluis/learning-management-system.git
   ```

2. Navigate to the project folder:
   ```bash
   cd "learning-management-system/Learning Management System"
   ```

3. Run the app:
   ```bash
   python main.py
   ```

4. Login with the default admin account:
   ```
   Email:    admin@lms.com
   Password: admin123
   ```

> 💡 On first run, 60+ PUP courses will be automatically seeded into the system.

---

## 🛠️ Built With

- **Python 3.x** — Core language
- **Tkinter** — GUI framework
- **JSON** — Data persistence
- **shutil / os / subprocess** — File and PDF handling

---

## 👩‍💻 Developers

- **Group 6**  
- **Course:** Object-Oriented Programming  
- **School:** Polytechnic University of the Philippines (PUP)

---

## 📄 License

This project is for educational purposes only.
