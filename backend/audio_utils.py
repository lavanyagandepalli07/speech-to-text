from pydub import AudioSegment

def stitch_audio(files: list[str], output_path: str):
    combined = AudioSegment.empty()

    for f in files:
        combined += AudioSegment.from_mp3(f)

    combined.export(output_path, format="mp3")
