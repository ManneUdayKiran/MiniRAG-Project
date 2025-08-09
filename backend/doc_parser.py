
import os
from fastapi import UploadFile
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        return file.file.read().decode(errors='ignore')

def extract_text_from_docx(file: UploadFile) -> str:
    file.file.seek(0)
    doc = Document(file.file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)
    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        print(f"[PDF Extract] Page {i+1} text: {repr(page_text[:200])}")
        text += page_text
    return text
