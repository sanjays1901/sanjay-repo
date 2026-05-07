from db import SessionLocal
from models import Document

from pdf_reader import extract_text_from_pdf
from chunker import chunk_text
from embedding_service import generate_embedding


session = SessionLocal()

# Step 1 - Extract text
text = extract_text_from_pdf(
    r"F:\PYTHON\chatbot\sample.pdf"
)

# Step 2 - Chunking
chunks = chunk_text(text)

# Step 3 - Store chunks
for chunk in chunks:

    embedding = generate_embedding(chunk)

    doc = Document(content=chunk, meta={"source": "sample.pdf"}, embedding=embedding)

    session.add(doc)

session.commit()

print("PDF ingested successfully!")

session.close()