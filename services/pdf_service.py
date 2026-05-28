import os
import shutil

class PDFService:
    def __init__(self, pdf_folder="data/pdfs"):
        self.pdf_folder = pdf_folder
        self.ensure_folder_exists()

    def ensure_folder_exists(self):
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)

    def upload_pdf(self, course, source_path):
        if not os.path.exists(source_path):
            return "PDF file not found!"
        if not source_path.endswith(".pdf"):
            return "File must be a PDF!"
        
        filename = f"course_{course.course_id}_{os.path.basename(source_path)}"
        destination = os.path.join(self.pdf_folder, filename)
        shutil.copy2(source_path, destination)
        course.attach_pdf(destination)
        return f"PDF uploaded successfully for {course.title}!"

    def download_pdf(self, course, destination_folder):
        if not course.pdf_file:
            return "No PDF attached to this course!"
        if not os.path.exists(course.pdf_file):
            return "PDF file not found!"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        filename = os.path.basename(course.pdf_file)
        destination = os.path.join(destination_folder, filename)
        shutil.copy2(course.pdf_file, destination)
        return f"PDF downloaded successfully to {destination}!"

    def delete_pdf(self, course):
        if not course.pdf_file:
            return "No PDF attached to this course!"
        if os.path.exists(course.pdf_file):
            os.remove(course.pdf_file)
            course.pdf_file = None
            return "PDF deleted successfully!"
        return "PDF file not found!"

    def get_pdf_path(self, course):
        if not course.pdf_file:
            return None
        return course.pdf_file