from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy import String

Base = declarative_base()

class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    meta = Column(JSONB)
    embedding = Column(Vector(1536))
    tenant_id = Column(String)

class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(String)

    session_id = Column(String)

    user_query = Column(Text)

    assistant_response = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )