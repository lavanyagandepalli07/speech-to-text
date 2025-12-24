import fitz  # PyMuPDF

def extract_text_pages(pdf_path: str):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        text = doc[i].get_text()
        yield i + 1, text.strip()
