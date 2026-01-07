"""
Database models and connection setup for the GOLD Profile Management Application.
"""

from sqlalchemy import create_engine, Column, String, Text, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import uuid

from app.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


class User(Base):
    """
    User model for storing profile information.

    This model represents a user in the GOLD e-commerce platform.
    Profile data is used for personalization in the recommendation engine.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    bio = Column(Text)
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default=dict)  # User preferences for recommendations
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


def get_db() -> Session:
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.

    This function should be called when the application starts
    to ensure all tables exist in the database.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all database tables.

    WARNING: This will delete all data. Use with caution.
    """
    Base.metadata.drop_all(bind=engine)
