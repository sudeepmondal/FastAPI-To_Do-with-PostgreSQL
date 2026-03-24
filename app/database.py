# ============================================================
# database.py - PostgreSQL connection using SQLAlchemy
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/tododb")

# Create the SQLAlchemy engine (connects to PostgreSQL)
engine = create_engine(DATABASE_URL)

# Each request gets its own session; auto-closed after use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all models will inherit from
Base = declarative_base()


# Dependency function for FastAPI routes
# Yields a DB session and ensures it closes after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()