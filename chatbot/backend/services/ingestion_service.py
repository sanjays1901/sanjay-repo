from db import SessionLocal
from models import Document

from pdf_reader import extract_text_from_pdf
from chunker import chunk_text
from embedding_service import generate_embedding
from datetime import datetime
from sqlalchemy import text
from db import engine


def ingest_pdf(file_path, filename, tenant_id="default"):

    with engine.connect() as conn:
        conn.execute(
            text("""
            DELETE FROM documents
            WHERE meta->>'source' = :filename
            """),
            {
                "filename": filename
            }
        )
        conn.commit()

    # Extract text
    pdf_text = extract_text_from_pdf(file_path)

    # Chunking
    chunks = chunk_text(pdf_text)

    session = SessionLocal()

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        doc = Document(content=chunk, 
                       tenant_id=tenant_id,
                       meta={ "source": filename, "chunk_index": index, "uploaded_at": str(datetime.utcnow())}, 
                       embedding=embedding)

        session.add(doc)

    session.commit()

    session.close()

    return len(chunks)