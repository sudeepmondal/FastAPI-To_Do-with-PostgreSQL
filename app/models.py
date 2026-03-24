# ============================================================
# models.py - SQLAlchemy ORM models (maps to DB tables)
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    Users table — stores registered users.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Automatically set when a user is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One user can have many tasks (one-to-many relationship)
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    """
    Tasks table — stores to-do tasks for each user.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    # Timestamps — automatically set on create and update
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign key linking each task to a user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to the User model
    owner = relationship("User", back_populates="tasks")