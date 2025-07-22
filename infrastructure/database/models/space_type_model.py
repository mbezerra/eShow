from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class SpaceTypeModel(Base):
    __tablename__ = "space_types"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 