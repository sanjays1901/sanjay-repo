import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import text
from db import engine
from embedding_service import generate_embedding
from pdf_reader import extract_text_from_pdf
from chunker import chunk_text
from models import Document
from db import SessionLocal
from services.retrieval_service import retrieve_chunks
from services.llm_service import generate_answer
from services.ingestion_service import ingest_pdf
from services.prompt_service import build_prompt
from config import Config
from services.chat_service import ask_question
from services.memory_service import (
    get_history,
    save_history
)
from services.chat_history_service import save_chat_history
from services.history_service import get_chat_history
from models import Base
import shutil

# Load env
load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QueryRequest(BaseModel):
    query: str
    tenant_id: str = "default"
    session_id: str | None = None

# API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory session store (replace with Redis later)
sessions = {}

@app.get("/")
def home():
    return {"status": "API is running"}

@app.post("/ask")
async def ask(req: QueryRequest):

    try:

        history = get_history(req.tenant_id, req.session_id)

        # Ask chatbot service
        result = ask_question(req.query, req.tenant_id, history)

        # Save conversation
        save_history(req.tenant_id, req.session_id, req.query, result["answer"])
        save_chat_history(req.tenant_id, req.session_id, req.query, result["answer"])
        return result

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="LLM error")

@app.post("/upload-pdf")
async def upload_pdf(tenant_id: str, file: UploadFile = File(...)):
    # Save file
    file_path = rf"{Config.UPLOAD_DIR}\{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    chunk_count = ingest_pdf(file_path, file.filename, tenant_id)
    return {"message": "PDF uploaded and ingested successfully", "chunks": chunk_count}

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM documents WHERE meta->>'source' = :filename"), {"filename": filename})
        conn.commit()
    return {
        "message": f"{filename} deleted successfully"
    }

@app.get("/documents")
async def list_documents():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT meta->>'source' AS source FROM documents ORDER BY source"))
        rows = result.fetchall()
    return {"documents": [row.source for row in rows]}

@app.get("/chat-history")
async def chat_history(
    tenant_id: str,
    session_id: str
):
    history = get_chat_history(tenant_id, session_id)
    return {"history": history}
# Run with: uvicorn main:app --reload --port 5000