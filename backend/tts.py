import os
import openai
from tenacity import retry, wait_exponential, stop_after_attempt

openai.api_key = os.getenv("OPENAI_API_KEY")

@retry(wait=wait_exponential(min=2, max=60), stop=stop_after_attempt(5))
def tts_openai(text: str, voice: str) -> bytes:
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    )
    return response.read()  # 🔥 FIX: return raw audio bytes
