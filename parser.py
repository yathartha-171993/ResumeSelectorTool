import pytesseract
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
from pdf2image import convert_from_path
import os

# Optional: Set tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_file(path):
    ext = path.split('.')[-1].lower()
    text = ""

    try:
        if ext == 'pdf':
            # Try text-based extraction first
            try:
                text = ""
                for page in fitz.open(path):
                    text += page.get_text()
                if not text.strip():
                    raise Exception("Empty text, fallback to OCR")
            except:
                # OCR fallback for scanned PDFs
                pages = convert_from_path(path)
                for page in pages:
                    text += pytesseract.image_to_string(page)

        elif ext == 'docx':
            doc = Document(path)
            for para in doc.paragraphs:
                text += para.text + '\n'

        elif ext in ['png', 'jpg', 'jpeg']:
            text = pytesseract.image_to_string(Image.open(path))

        else:
            text = "[Unsupported file type]"

    except Exception as e:
        text = f"[Error reading file: {e}]"

    return text

def score_resume(text, selected_skills):
    score = 0
    text = text.lower()
    for skill in selected_skills:
        if skill.lower() in text:
            score += 1
    return score
