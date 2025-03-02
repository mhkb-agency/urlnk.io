from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Fetch database URL from environment variables (set by Docker Compose)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://urlnk_user:urlnk_password@db/urlnk_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    """
    SQLAlchemy model for storing shortened URLs and metadata.
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    click_count = Column(Integer, default=0)

# Create the database tables
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Database session generator for dependency injection in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
