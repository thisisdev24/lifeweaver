
"""Extended extractors for PDFs, OCR, and audio transcription with safe fallbacks.

Functions:
- extract_text_from_pdf(path)
- extract_text_from_image(path)  # OCR
- transcribe_audio(path)         # whisper or fallback stub
"""
import os
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None

# whisper is optional and heavy; provide stub if missing
try:
    import whisper
except Exception:
    whisper = None

def extract_text_from_pdf(path: str) -> str:
    if fitz is None:
        raise RuntimeError('PyMuPDF not installed. Install with pip install PyMuPDF')
    doc = fitz.open(path)
    pages = []
    for p in doc:
        pages.append(p.get_text())
    return '\n'.join(pages)

def extract_text_from_image(path: str) -> str:
    if pytesseract is None or Image is None:
        raise RuntimeError('pytesseract or Pillow not installed. Install pytesseract and Pillow')
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return text

def transcribe_audio(path: str) -> str:
    if whisper is None:
        # fallback: return an informative stub so pipeline continues
        return '[transcription not available - whisper not installed]'
    model = whisper.load_model('small')  # consider tiny/tiny.en for speed
    res = model.transcribe(path)
    return res.get('text','')
