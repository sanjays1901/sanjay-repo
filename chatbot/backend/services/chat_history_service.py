from sqlalchemy import text
from db import engine

def save_chat_history(tenant_id, session_id, query,answer):

    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO chat_history (
                tenant_id,
                session_id,
                user_query,
                assistant_response
            ) VALUES (
                :tenant_id,
                :session_id,
                :query,
                :answer
            )
            """),
            {
                "tenant_id": tenant_id,
                "session_id": session_id,
                "query": query,
                "answer": answer
            }
        )

        conn.commit()