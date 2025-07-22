from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class FestivalTypeModel(Base):
    __tablename__ = "festival_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 