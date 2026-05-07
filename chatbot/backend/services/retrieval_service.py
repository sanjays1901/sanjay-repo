from sqlalchemy import text
from db import engine
from embedding_service import generate_embedding


def retrieve_chunks(query, tenant_id="default", limit=3):

    query_embedding = generate_embedding(query)

    sql = text("""
    SELECT
        content,
        meta,
        embedding <=> CAST(:embedding AS vector) AS distance
    FROM documents
    WHERE
        embedding <=> CAST(:embedding AS vector) < 0.6
        OR
        content ILIKE :keyword
        AND tenant_id = :tenant_id
    ORDER BY distance
    LIMIT :limit;
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"embedding": str(query_embedding), "keyword": f"%{query}%", "tenant_id": tenant_id, "limit": limit})
        rows = result.fetchall()

    for row in rows:
        print(row.distance, row.meta)
    return rows