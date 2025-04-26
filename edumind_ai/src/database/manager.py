"""
Database management functionality.
"""
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from .models import Base, Document, Chapter, Session, Interaction, Progress

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path=None):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file (if None, uses a default path)
        """
        if db_path is None:
            # Default to a db file in the project root
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(root_dir, 'edumind.db')
        
        logger.info(f"Initializing database at {db_path}")
        
        # Create 'sqlite:///path/to/db' connection string
        db_uri = f"sqlite:///{db_path}"
        
        # Create engine and session factory
        self.engine = create_engine(db_uri, echo=False)
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
    
    def init_db(self):
        """Initialize the database schema."""
        logger.info("Creating database tables")
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    # Document operations
    def add_document(self, filename, file_path, title=None):
        """
        Add a new document to the database.
        
        Args:
            filename: Original filename
            file_path: Path to the stored file
            title: Document title (if available)
            
        Returns:
            Document object
        """
        session = self.get_session()
        try:
            document = Document(
                filename=filename,
                file_path=file_path,
                title=title
            )
            session.add(document)
            session.commit()
            return document
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_document(self, document_id):
        """
        Get a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document object or None
        """
        session = self.get_session()
        try:
            return session.query(Document).get(document_id)
        finally:
            session.close()
    
    def get_all_documents(self):
        """
        Get all documents.
        
        Returns:
            List of Document objects
        """
        session = self.get_session()
        try:
            return session.query(Document).all()
        finally:
            session.close()
    
    # Chapter operations
    def add_chapter(self, document_id, title, content, page_start=None, page_end=None):
        """
        Add a chapter to a document.
        
        Args:
            document_id: Document ID
            title: Chapter title
            content: Chapter text content
            page_start: Starting page number
            page_end: Ending page number
            
        Returns:
            Chapter object
        """
        session = self.get_session()
        try:
            chapter = Chapter(
                document_id=document_id,
                title=title,
                content=content,
                page_start=page_start,
                page_end=page_end
            )
            session.add(chapter)
            session.commit()
            return chapter
        except Exception as e:
            logger.error(f"Error adding chapter: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    # Session operations
    def start_session(self, document_id):
        """
        Start a new learning session.
        
        Args:
            document_id: Document ID
            
        Returns:
            Session object
        """
        session = self.get_session()
        try:
            learning_session = Session(document_id=document_id)
            session.add(learning_session)
            session.commit()
            return learning_session
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def end_session(self, session_id):
        """
        End a learning session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Updated Session object
        """
        session = self.get_session()
        try:
            learning_session = session.query(Session).get(session_id)
            if learning_session:
                learning_session.ended_at = datetime.datetime.utcnow()
                session.commit()
            return learning_session
        except Exception as e:
            logger.error(f"Error ending session: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    # Interaction operations
    def add_interaction(self, session_id, question, answer=None, confidence=None, is_ai_generated=False):
        """
        Add a question-answer interaction.
        
        Args:
            session_id: Session ID
            question: Question text
            answer: Answer text (if available)
            confidence: Confidence score (0-1)
            is_ai_generated: Whether this is an AI-generated comprehension question
            
        Returns:
            Interaction object
        """
        session = self.get_session()
        try:
            interaction = Interaction(
                session_id=session_id,
                question=question,
                answer=answer,
                confidence=confidence,
                is_ai_generated=is_ai_generated
            )
            session.add(interaction)
            session.commit()
            return interaction
        except Exception as e:
            logger.error(f"Error adding interaction: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    # Progress operations
    def update_progress(self, session_id, chapter_id, completed=False, comprehension_score=None):
        """
        Update learning progress.
        
        Args:
            session_id: Session ID
            chapter_id: Chapter ID
            completed: Whether the chapter has been completed
            comprehension_score: Score representing comprehension level (0-1)
            
        Returns:
            Progress object
        """
        session = self.get_session()
        try:
            # Check if a progress entry already exists
            progress = session.query(Progress).filter_by(
                session_id=session_id, 
                chapter_id=chapter_id
            ).first()
            
            if progress:
                # Update existing progress
                progress.completed = completed
                if comprehension_score is not None:
                    progress.comprehension_score = comprehension_score
                progress.timestamp = datetime.datetime.utcnow()
            else:
                # Create new progress entry
                progress = Progress(
                    session_id=session_id,
                    chapter_id=chapter_id,
                    completed=completed,
                    comprehension_score=comprehension_score
                )
                session.add(progress)
            
            session.commit()
            return progress
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
            session.rollback()
            raise
        finally:
            session.close()
