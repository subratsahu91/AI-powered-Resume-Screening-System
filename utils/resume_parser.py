from pypdf import PdfReader
from docx import Document

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])

    if file.name.endswith(".docx"):
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    return ""
