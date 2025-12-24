import streamlit as st
import requests
import time
import os

API_URL = os.getenv("API_URL", "http://backend:8000")

st.set_page_config(page_title="PDF to Audiobook", layout="wide")
st.title("📘 PDF → Audiobook")

voice = st.sidebar.selectbox(
    "Select Voice",
    ["alloy", "echo", "shimmer"]
)

pdf = st.file_uploader("Upload PDF", type=["pdf"])

if pdf:
    res = requests.post(
        f"{API_URL}/submit",
        files={"pdf": pdf},
        data={"voice": voice}
    )

    job_id = res.json()["job_id"]
    progress = st.progress(0)
    status_box = st.empty()

    while True:
        status = requests.get(f"{API_URL}/status/{job_id}").json()

        if status["state"] == "PROGRESS":
            page = status["meta"]["page"]
            progress.progress(min(page / 1000, 1.0))
            status_box.info(f"Processing page {page}")

        if status["state"] == "SUCCESS":
            st.success("🎧 Audiobook ready!")
            audio = requests.get(f"{API_URL}/download/{job_id}").content

            st.download_button(
                "Download MP3",
                audio,
                file_name="audiobook.mp3"
            )
            break

        if status["state"] == "FAILURE":
            st.error("Processing failed.")
            break

        time.sleep(2)
