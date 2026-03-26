from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)

class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    name = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    is_private = Column(Boolean, default=False)

class CodeEmbedding(Base):
    __tablename__ = 'code_embeddings'
    id = Column(Integer, primary_key=True)
    file_path = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    repository_id = Column(String(100), index=True, nullable=False)
    # text-embedding-004 do Google tem 768 dimensões nativamente
    embedding = Column(Vector(768))
