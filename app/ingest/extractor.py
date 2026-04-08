import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from app.db.session import SessionLocal
from app.ingest.models import Document


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""

    for page in doc:
        text = page.get_text()

        # If no text found, use OCR
        if not text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)

        full_text += text + "\n"

    return full_text


def process_extraction(file_path):
    filename = os.path.basename(file_path)

    if file_path.lower().endswith(".txt"):
        content = extract_text_from_txt(file_path)

    elif file_path.lower().endswith(".pdf"):
        content = extract_text_from_pdf(file_path)

    else:
        return

    db = SessionLocal()
    document = Document(filename=filename, content=content)
    db.add(document)
    db.commit()
    db.close()

    print(f"Extracted and saved: {filename}")


# import os
# from typing import Optional

# try:
#     import fitz  # PyMuPDF
# except Exception:
#     fitz = None


# def extract_text_from_pdf(path: str) -> str:
#     if fitz is None:
#         raise RuntimeError("PyMuPDF not installed")
#     doc = fitz.open(path)
#     txt = []
#     for page in doc:
#         txt.append(page.get_text())
#     return "\n".join(txt)
