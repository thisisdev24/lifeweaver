import os
from typing import Optional

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None


def extract_text_from_pdf(path: str) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")
    doc = fitz.open(path)
    txt = []
    for page in doc:
        txt.append(page.get_text())
    return "\n".join(txt)
