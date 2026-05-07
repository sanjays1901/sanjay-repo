from pdf_reader import extract_text_from_pdf
from chunker import chunk_text

text = extract_text_from_pdf(
    r"F:\PYTHON\chatbot\sample.pdf"
)

chunks = chunk_text(text)

for i, chunk in enumerate(chunks):

    print(f"\n--- CHUNK {i+1} ---\n")

    print(chunk)