from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Fetch database URL from environment variables (set by Docker Compose)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://urlnk_user:urlnk_password@db/urlnk_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Database session generator for dependency injection in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
