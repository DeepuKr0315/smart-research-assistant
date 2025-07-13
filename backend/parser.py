import pdfplumber
import os

def read_document(file_path):
    if file_path.endswith('.pdf'):
        try:
            text = ''
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
    
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Error reading TXT: {e}")
    
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT.")