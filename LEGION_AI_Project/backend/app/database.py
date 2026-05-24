"""
Database configuration and session management.

For the MVP we use SQLite for simplicity.  In production you should
configure PostgreSQL or another robust RDBMS via the `DATABASE_URL`
environment variable.  SQLAlchemy models are defined in `models.py`.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./legion_ai.db")

# SQLite needs special handling for multithreading; check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()