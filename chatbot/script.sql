CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    meta JSONB,
    embedding VECTOR(1536)
);

SELECT id, content, meta
FROM documents;

ALTER TABLE documents
ADD COLUMN tenant_id TEXT;

CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    tenant_id TEXT,
    session_id TEXT,
    user_query TEXT,
    assistant_response TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

SELECT *
FROM chat_history
ORDER BY created_at DESC;