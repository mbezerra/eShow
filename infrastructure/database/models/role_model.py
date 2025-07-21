from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base
from domain.entities.role import RoleType

class RoleModel(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(SQLAlchemyEnum(RoleType), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com Profile (importação local para evitar erro de importação circular)
    profiles = relationship("ProfileModel", back_populates="role") 