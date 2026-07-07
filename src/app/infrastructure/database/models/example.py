from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.infrastructure.database.core import Base


class ExampleModel(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
