from sqlalchemy import text
from db import engine
from embedding_service import generate_embedding

query = "Can I return a product?"

query_embedding = generate_embedding(query)

#cosine distance operator
sql = text("""
SELECT
    content,
    meta,
    embedding <=> CAST(:embedding AS vector) AS distance
FROM documents
ORDER BY distance
LIMIT 5;
""")

with engine.connect() as conn:
    result = conn.execute(sql, {"embedding": str(query_embedding)})
    rows = result.fetchall()

    for row in rows:
        print("\nCONTENT:")
        print(row.content)

        print("\nMETA:")
        print(row.meta)

        print("\nDISTANCE:")
        print(row.distance)