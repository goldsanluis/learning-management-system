# ============================================================
# main.py - Application Entry Point
# Starts the LMS by:
# 1. Loading saved data from file
# 2. Showing the login window
# 3. Launching the main window after successful login
# ============================================================

from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from services.enrollment_service import EnrollmentService
from services.pdf_service import PDFService
from file_handler.file_manager import FileManager

def main():
    # Initialize all services
    service = EnrollmentService()
    pdf_service = PDFService()
    file_manager = FileManager()

    # Load all previously saved data into the service
    file_manager.load_data(service)

    # Ensure there is always a default instructor account
    if not service.get_instructor_by_email("admin@lms.com"):
        service.add_instructor("Admin Instructor", "admin@lms.com", "admin123")
        file_manager.save_data(service)

    # Seed PUP courses if none exist yet
    if not service.get_all_courses():
        admin = service.get_instructor_by_email("admin@lms.com")

        pup_courses = [
            # College of Computer and Information Sciences (CCIS)
            ("BSCS - Bachelor of Science in Computer Science", "Core CS program covering algorithms, software engineering, and systems.", admin),
            ("BSIT - Bachelor of Science in Information Technology", "IT program covering networking, web systems, and database management.", admin),

            # College of Engineering (CE)
            ("BSCE - Bachelor of Science in Civil Engineering", "Covers structural, geotechnical, and environmental engineering.", admin),
            ("BSCpE - Bachelor of Science in Computer Engineering", "Combines hardware and software engineering principles.", admin),
            ("BSEE - Bachelor of Science in Electrical Engineering", "Covers power systems, electronics, and electrical design.", admin),
            ("BSECE - Bachelor of Science in Electronics Engineering", "Focuses on communication systems and electronic devices.", admin),
            ("BSIE - Bachelor of Science in Industrial Engineering", "Covers production systems, operations research, and quality management.", admin),
            ("BSME - Bachelor of Science in Mechanical Engineering", "Covers thermodynamics, machine design, and manufacturing.", admin),
            ("BSRE - Bachelor of Science in Railway Engineering", "Specialized program on railway infrastructure and management.", admin),

            # College of Accountancy and Finance (CAF)
            ("BSA - Bachelor of Science in Accountancy", "Covers financial accounting, auditing, and taxation.", admin),
            ("BSMA - Bachelor of Science in Management Accounting", "Focuses on managerial and cost accounting.", admin),
            ("BSBAFM - BS Business Administration major in Financial Management", "Covers banking, investments, and financial planning.", admin),

            # College of Business Administration (CBA)
            ("BSBAHRM - BS Business Administration major in Human Resource Management", "Covers recruitment, labor relations, and organizational behavior.", admin),
            ("BSBAMM - BS Business Administration major in Marketing Management", "Covers marketing strategy, consumer behavior, and branding.", admin),
            ("BSENTREP - Bachelor of Science in Entrepreneurship", "Covers business planning, innovation, and startup management.", admin),
            ("BSOA - Bachelor of Science in Office Administration", "Covers office systems, records management, and business communication.", admin),

            # College of Arts and Letters (CAL)
            ("ABELS - Bachelor of Arts in English Language Studies", "Covers linguistics, literature, and communication.", admin),
            ("ABF - Bachelor of Arts in Filipinology", "Covers Filipino language, culture, and literature.", admin),
            ("ABLCS - Bachelor of Arts in Literary and Cultural Studies", "Covers literary theory and cultural analysis.", admin),
            ("AB-PHILO - Bachelor of Arts in Philosophy", "Covers logic, ethics, and philosophical traditions.", admin),
            ("BPEA - Bachelor of Performing Arts major in Theater Arts", "Covers acting, directing, and stage production.", admin),

            # College of Communication (COC)
            ("BADPR - Bachelor in Advertising and Public Relations", "Covers advertising strategy, PR campaigns, and media.", admin),
            ("BA Broadcasting", "Covers radio, TV production, and broadcast journalism.", admin),
            ("BACR - Bachelor of Arts in Communication Research", "Covers research methods in media and communication.", admin),
            ("BAJ - Bachelor of Arts in Journalism", "Covers news writing, investigative reporting, and media ethics.", admin),

            # College of Science (CS)
            ("BSAPMATH - Bachelor of Science in Applied Mathematics", "Covers calculus, statistics, and mathematical modeling.", admin),
            ("BSBIO - Bachelor of Science in Biology", "Covers cell biology, genetics, and ecology.", admin),
            ("BSCHEM - Bachelor of Science in Chemistry", "Covers organic, inorganic, and analytical chemistry.", admin),
            ("BSMATH - Bachelor of Science in Mathematics", "Covers pure mathematics including algebra and analysis.", admin),
            ("BSND - Bachelor of Science in Nutrition and Dietetics", "Covers human nutrition, food science, and dietetic practice.", admin),
            ("BSPHY - Bachelor of Science in Physics", "Covers classical mechanics, electromagnetism, and modern physics.", admin),
            ("BSSTAT - Bachelor of Science in Statistics", "Covers statistical theory, data analysis, and probability.", admin),
            ("BSFT - Bachelor of Science in Food Technology", "Covers food processing, safety, and quality control.", admin),

            # College of Education (COED)
            ("BEEd - Bachelor of Elementary Education", "Prepares teachers for elementary school instruction.", admin),
            ("BECEd - Bachelor of Early Childhood Education", "Covers early childhood development and teaching methods.", admin),
            ("BSEd-English - Bachelor of Secondary Education major in English", "Prepares English teachers for secondary school.", admin),
            ("BSEd-Math - Bachelor of Secondary Education major in Mathematics", "Prepares math teachers for secondary school.", admin),
            ("BSEd-Science - Bachelor of Secondary Education major in Science", "Prepares science teachers for secondary school.", admin),
            ("BLIS - Bachelor of Library and Information Science", "Covers library management, cataloging, and information systems.", admin),

            # College of Architecture, Design and the Built Environment (CADBE)
            ("BS-ARCH - Bachelor of Science in Architecture", "Covers architectural design, building technology, and urban planning.", admin),
            ("BSID - Bachelor of Science in Interior Design", "Covers space planning, design principles, and materials.", admin),
            ("BSEP - Bachelor of Science in Environmental Planning", "Covers land use, urban development, and environmental policy.", admin),

            # College of Social Sciences and Development (CSSD)
            ("ABS - Bachelor of Arts in Sociology", "Covers social theory, research methods, and social institutions.", admin),
            ("BSE - Bachelor of Science in Economics", "Covers micro and macroeconomics, econometrics, and policy.", admin),
            ("BAH - Bachelor of Arts in History", "Covers Philippine and world history and historiography.", admin),
            ("BSPSY - Bachelor of Science in Psychology", "Covers human behavior, mental processes, and research methods.", admin),
            ("BSSW - Bachelor of Science in Social Work", "Covers community development, welfare services, and counseling.", admin),

            # College of Political Science and Public Administration (CPSPA)
            ("BAPS - Bachelor of Arts in Political Science", "Covers political theory, governance, and comparative politics.", admin),
            ("BAPE - Bachelor of Arts in Political Economy", "Covers the relationship between politics and economic systems.", admin),
            ("BAIS - Bachelor of Arts in International Studies", "Covers international relations, diplomacy, and global issues.", admin),
            ("BPA - Bachelor of Public Administration", "Covers public policy, government administration, and ethics.", admin),

            # College of Tourism, Hospitality and Transportation Management (CTHTM)
            ("BSHM - Bachelor of Science in Hospitality Management", "Covers hotel operations, food service, and event management.", admin),
            ("BSTM - Bachelor of Science in Tourism Management", "Covers travel operations, tour guiding, and tourism planning.", admin),
            ("BSTRM - Bachelor of Science in Transportation Management", "Covers logistics, transport systems, and fleet management.", admin),

            # College of Human Kinetics (CHK)
            ("BPE - Bachelor of Physical Education", "Covers physical fitness, sports coaching, and kinesiology.", admin),
            ("BSESS - Bachelor of Science in Exercise and Sports Sciences", "Covers sports science, performance training, and rehabilitation.", admin),

            # College of Law (CL)
            ("JD - Juris Doctor", "Professional law degree covering civil, criminal, and constitutional law.", admin),

            # Graduate School - Master's
            ("MBA - Master in Business Administration", "Advanced business program covering strategy, finance, and leadership.", admin),
            ("MSIT - Master of Science in Information Technology", "Graduate IT program with specializations in data analytics and security.", admin),
            ("MSCS-equivalent - Master of Science in Computer Engineering", "Graduate program in applied security, data science, and engineering.", admin),
            ("MPA - Master in Public Administration", "Graduate program in governance, policy analysis, and public management.", admin),
            ("MAP - Master of Arts in Psychology", "Graduate psychology with clinical and industrial specializations.", admin),
        ]

        for title, description, instructor in pup_courses:
            service.add_course(title, description, instructor)

        file_manager.save_data(service)
        print(f"Seeded {len(pup_courses)} PUP courses.")


    def on_login_success(user, role):
        # Called by LoginWindow after a successful login
        # Launch the main application window
        app = MainWindow(user, role, service, pdf_service, file_manager)
        app.run()

    # Show the login screen first
    login = LoginWindow(service, file_manager, on_login_success)
    login.run()

if __name__ == "__main__":
    main()
