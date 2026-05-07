from db import SessionLocal
from models import Document
from embedding_service import generate_embedding

session = SessionLocal()

text = """
Our refund policy allows returns within 30 days.
"""

embedding = generate_embedding(text)

doc = Document(
    content=text,
    meta ={"source": "policy.txt"},
    embedding=embedding
)

session.add(doc)
session.commit()

print("Document inserted successfully!")

session.close()