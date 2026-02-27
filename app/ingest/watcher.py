# import os, shutil, uuid
# from fastapi import UploadFile

# ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# INGEST_DIR = os.path.join(ROOT, "data", "ingest")
# os.makedirs(INGEST_DIR, exist_ok=True)


# async def save_uploaded_file(file: UploadFile) -> str:
#     ext = os.path.splitext(file.filename)[1]
#     uid = str(uuid.uuid4())[:8]
#     dest = os.path.join(INGEST_DIR, f"{uid}{ext}")
#     with open(dest, "wb") as f:
#         content = await file.read()
#         f.write(content)
#     return dest


# def simple_import(path: str) -> str:
#     """Copy a local file into ingest area (used for CLI)."""
#     if not os.path.exists(path):
#         raise FileNotFoundError(path)
#     dest = os.path.join(INGEST_DIR, os.path.basename(path))
#     shutil.copy2(path, dest)
#     return dest

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.api.ingest import process_file, WATCH_DIR


class IngestHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            process_file(event.dest_path)

from app.db.database import Base, engine
Base.metadata.create_all(bind=engine)


def main():
    # ensure the watch directory exists before starting observer
    if not os.path.exists(WATCH_DIR):
        raise FileNotFoundError(
            f"Watch directory {WATCH_DIR!r} does not exist. "
            "update WATCH_DIR in app.api.ingest or create the path."
        )

    event_handler = IngestHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()

    print(f"Watching {WATCH_DIR} for PDF and TXT files")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()