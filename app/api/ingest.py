# from fastapi import APIRouter, UploadFile, File
# from app.ingest.watcher import save_uploaded_file

# router = APIRouter()


# @router.post("/file")
# async def ingest_file(file: UploadFile = File(...)):
#     path = await save_uploaded_file(file)
#     return {"status": "ok", "path": path}

import os
import shutil
import time
from app.ingest.extractor import process_extraction

WATCH_DIR = os.getenv("WATCH_DIR", "/workspaces/lifeweaver/data/watch")
INGEST_DIR = os.getenv("INGEST_DIR", "/workspaces/lifeweaver/data/ingest")
ALLOWED_EXTENSIONS = (".pdf", ".txt")


def wait_for_file_complete(file_path):
    previous_size = -1
    while True:
        current_size = os.path.getsize(file_path)
        if current_size == previous_size:
            break
        previous_size = current_size
        time.sleep(1)


def process_file(file_path):
    if not os.path.isfile(file_path):
        return

    if not file_path.lower().endswith(ALLOWED_EXTENSIONS):
        return

    wait_for_file_complete(file_path)

    filename = os.path.basename(file_path)
    destination = os.path.join(INGEST_DIR, filename)

    if not os.path.exists(INGEST_DIR):
        raise Exception("Ingest directory does not exist. Create D:\\Lifeweaver\\ingest first.")

    if os.path.exists(destination):
        print(f"Skipped: {filename}")
        return

    shutil.copy2(file_path, destination)
    print(f"Copied: {filename}")

    process_extraction(destination)