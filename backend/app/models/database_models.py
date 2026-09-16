from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    role = Column(String(20), default="student") # "student" or "admin"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    chats = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch = Column(String(100), default="Computer Engineering")
    cgpa = Column(Float, default=7.2)
    graduation_year = Column(Integer, default=2027)
    backlogs = Column(Integer, default=1)
    skills = Column(String(500), default="Python, C++, SQL, HTML, CSS")
    preferred_role = Column(String(100), default="Data Analyst")
    
    user = relationship("User", back_populates="profile")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # e.g. "Company Notices", "Placement Rules"
    company = Column(String(100), nullable=True) # e.g. "Demo Company B"
    upload_date = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer, default=0)
    status = Column(String(50), default="indexed") # "indexed", "processing", "failed"
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_id = Column(String(100), unique=True, index=True, nullable=False) # Unique string key
    vector_id = Column(Integer, unique=True, nullable=True) # Mapping to FAISS vector index position
    page_number = Column(Integer, default=1)
    category = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    text = Column(Text, nullable=False)
    
    document = relationship("Document", back_populates="chunks")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="chats")
