from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from celery.result import AsyncResult
from tasks import process_pdf
import os

app = FastAPI()

DATA_DIR = "/data"

@app.post("/submit")
async def submit(pdf: UploadFile, voice: str = "alloy"):
    task = process_pdf.delay(await pdf.read(), voice)
    return {"job_id": task.id}

@app.get("/status/{job_id}")
def status(job_id: str):
    task = AsyncResult(job_id)
    return {
        "state": task.state,
        "meta": task.info
    }

@app.get("/download/{job_id}")
def download(job_id: str):
    path = os.path.join(DATA_DIR, job_id, "audiobook.mp3")
    return FileResponse(path, media_type="audio/mpeg", filename="audiobook.mp3")
