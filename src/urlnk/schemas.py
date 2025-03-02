from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


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
