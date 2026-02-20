from fastapi import APIRouter, UploadFile, File
from app.ingest.watcher import save_uploaded_file

router = APIRouter()


@router.post("/file")
async def ingest_file(file: UploadFile = File(...)):
    path = await save_uploaded_file(file)
    return {"status": "ok", "path": path}
