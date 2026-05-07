from fastapi import FastAPI
from sqlalchemy import text
from db import engine
from embedding_service import generate_embedding
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.post("/ask")
def ask(data: dict):

    query = data["query"]

    query_embedding = generate_embedding(query)

    sql = text("""
    SELECT
        content,
        meta,
        embedding <=> CAST(:embedding AS vector) AS distance
    FROM documents
    ORDER BY distance
    LIMIT 3;
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {"embedding": str(query_embedding)})
        rows = result.fetchall()

    context = "\n\n".join([row.content for row in rows])

    prompt = f"""
    You are an enterprise AI assistant.

    Answer ONLY from provided context.

    If answer not found in context,
    say:
    "I could not find this in knowledge base."

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """

    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])

    return {"answer": response.choices[0].message.content, "sources": [row.meta for row in rows]}