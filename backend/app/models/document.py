from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    template_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    field_values = Column(JSON, default={})
    status = Column(String, default="draft")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Document(id={self.id}, user_id={self.user_id}, template_id={self.template_id})>"
