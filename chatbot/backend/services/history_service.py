from sqlalchemy import text
from db import engine

def get_chat_history(tenant_id, session_id):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                user_query,
                assistant_response,
                created_at
            FROM chat_history
            WHERE
                tenant_id = :tenant_id
                AND session_id = :session_id
            ORDER BY created_at
            """),
            {
                "tenant_id": tenant_id,
                "session_id": session_id
            }
        )

        rows = result.fetchall()

    return [{"query": row.user_query, "answer": row.assistant_response, "created_at": str(row.created_at)} for row in rows]