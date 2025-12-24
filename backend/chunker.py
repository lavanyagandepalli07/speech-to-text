import re

MAX_CHARS = 4000

def sentence_chunker(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    buffer = []
    size = 0

    for s in sentences:
        if size + len(s) <= MAX_CHARS:
            buffer.append(s)
            size += len(s)
        else:
            yield " ".join(buffer)
            buffer = [s]
            size = len(s)

    if buffer:
        yield " ".join(buffer)
