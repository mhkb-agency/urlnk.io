from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import HttpUrl

from .database import Base


class URL(Base):
    """
    SQLAlchemy model for storing shortened URLs and metadata.
    """
    __tablename__ = "urls"

    id: int = Column(Integer, primary_key=True, index=True)
    short_code: str = Column(String(10), unique=True, index=True, nullable=False)
    long_url: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))
    click_count: int = Column(Integer, default=0)

    def get_long_http_url(self) -> HttpUrl:
        return HttpUrl(self.long_url)
