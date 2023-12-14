from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from sqlalchemy.dialects.postgresql import UUID
from src.db.db import Base


class UrlsClick(Base):
    __tablename__ = 'urls_clicks'
    id = Column(Integer, primary_key=True)
    url_id = Column(ForeignKey('urls.id', ondelete='CASCADE'))
    client_host = Column(String(50), nullable=False)
    client_port = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Urls(Base):
    __tablename__ = "urls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    original_url = Column(URLType, nullable=False)
    clicks = relationship("UrlsClick", backref='url', cascade="all, delete")
    deleted = Column(Boolean, default=False)