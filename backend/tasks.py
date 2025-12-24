from celery import Celery
import os, tempfile

from pdf_utils import extract_text_pages
from chunker import sentence_chunker
from tts import tts_openai
from audio_utils import stitch_audio

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

DATA_DIR = "/data"

@celery.task(bind=True)
def process_pdf(self, pdf_bytes: bytes, voice: str):
    job_id = self.request.id
    job_dir = os.path.join(DATA_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    pdf_path = os.path.join(job_dir, "book.pdf")

    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    audio_chunks = []

    for page_num, text in extract_text_pages(pdf_path):
        if len(text.strip()) < 20:
            raise ValueError("Scanned PDF detected. OCR required.")

        self.update_state(
            state="PROGRESS",
            meta={"page": page_num}
        )

        for idx, chunk in enumerate(sentence_chunker(text)):
            audio_bytes = tts_openai(chunk, voice)
            chunk_path = os.path.join(job_dir, f"{page_num}_{idx}.mp3")

            with open(chunk_path, "wb") as f:
                f.write(audio_bytes)

            audio_chunks.append(chunk_path)

    output_path = os.path.join(job_dir, "audiobook.mp3")
    stitch_audio(audio_chunks, output_path)

    return {
        "output": output_path,
        "status": "completed"
    }
