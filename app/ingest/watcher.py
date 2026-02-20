import os, shutil, uuid
from fastapi import UploadFile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INGEST_DIR = os.path.join(ROOT, "data", "ingest")
os.makedirs(INGEST_DIR, exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1]
    uid = str(uuid.uuid4())[:8]
    dest = os.path.join(INGEST_DIR, f"{uid}{ext}")
    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)
    return dest


def simple_import(path: str) -> str:
    """Copy a local file into ingest area (used for CLI)."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    dest = os.path.join(INGEST_DIR, os.path.basename(path))
    shutil.copy2(path, dest)
    return dest
