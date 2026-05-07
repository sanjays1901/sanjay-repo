from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text
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