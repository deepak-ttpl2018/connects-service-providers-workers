"""
Database models for EduMind AI.
"""
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Document(Base):
    """Model representing an uploaded document."""
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    title = Column(String(255))
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    chapters = relationship("Chapter", back_populates="document", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="document")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}')>"

class Chapter(Base):
    """Model representing a chapter or section in a document."""
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    page_start = Column(Integer)
    page_end = Column(Integer)
    
    # Relationships
    document = relationship("Document", back_populates="chapters")
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, title='{self.title}')>"

class Session(Base):
    """Model representing a learning session."""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime)
    current_chapter_id = Column(Integer, ForeignKey('chapters.id'))
    
    # Relationships
    document = relationship("Document", back_populates="sessions")
    interactions = relationship("Interaction", back_populates="session", cascade="all, delete-orphan")
    current_chapter = relationship("Chapter")
    
    def __repr__(self):
        return f"<Session(id={self.id}, started_at='{self.started_at}')>"

class Interaction(Base):
    """Model representing a question-answer interaction."""
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    confidence = Column(Float)
    is_ai_generated = Column(Boolean, default=False)  # False for student questions, True for AI-generated comprehension questions
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="interactions")
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, question='{self.question[:20]}...')>"

class Progress(Base):
    """Model for tracking student progress."""
    __tablename__ = 'progress'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    completed = Column(Boolean, default=False)
    comprehension_score = Column(Float)  # 0-1 scale
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    session = relationship("Session")
    chapter = relationship("Chapter")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, chapter_id={self.chapter_id}, completed={self.completed})>"
