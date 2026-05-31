# ============================================================
# pdf_service.py - PDFService class
# Handles all PDF file operations: upload, download, delete.
# Stores PDFs in the data/pdfs folder.
# ============================================================

import os
import shutil
import subprocess
import sys


class PDFService:
    def __init__(self, pdf_folder="data/pdfs"):
        self.pdf_folder = pdf_folder
        self.ensure_folder_exists()

    def ensure_folder_exists(self):
        # Create the PDF storage folder if it doesn't exist
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)

    def upload_pdf(self, course, source_path):
        # Validate the file exists and is a PDF
        if not os.path.exists(source_path):
            return "PDF file not found!"
        if not source_path.lower().endswith(".pdf"):
            return "File must be a PDF!"

        # Copy the PDF into the system's pdf folder with a unique name
        filename = f"course_{course.course_id}_{os.path.basename(source_path)}"
        destination = os.path.join(self.pdf_folder, filename)
        shutil.copy2(source_path, destination)

        # Attach the stored path to the course object
        course.attach_pdf(destination)
        return f"PDF uploaded successfully for {course.title}!"

    def download_pdf(self, course, destination_folder):
        # Check that the course has a PDF attached
        if not course.pdf_file:
            return "No PDF attached to this course!"
        if not os.path.exists(course.pdf_file):
            return "PDF file not found on server!"

        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Copy the PDF to the chosen destination
        filename = os.path.basename(course.pdf_file)
        destination = os.path.join(destination_folder, filename)
        shutil.copy2(course.pdf_file, destination)
        return f"PDF downloaded successfully to {destination}!"

    def open_pdf(self, course):
        if not course.pdf_file:
            return "No PDF attached to this course!"
        if not os.path.exists(course.pdf_file):
            return "PDF file not found!"
        
        import subprocess
        import sys
        
        if sys.platform == "win32":
            os.startfile(course.pdf_file)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", course.pdf_file])
        else:
            subprocess.Popen(["xdg-open", course.pdf_file])
        
        return "Opening PDF..."



    def delete_pdf(self, course):
        # Delete the PDF file and remove the reference from the course
        if not course.pdf_file:
            return "No PDF attached to this course!"
        if os.path.exists(course.pdf_file):
            os.remove(course.pdf_file)
            course.pdf_file = None
            return "PDF deleted successfully!"
        return "PDF file not found!"

    def get_pdf_path(self, course):
        # Return the file path of the course's PDF, or None
        if not course.pdf_file:
            return None
        return course.pdf_file
