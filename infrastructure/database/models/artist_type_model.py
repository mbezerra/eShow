from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base
from domain.entities.artist_type import ArtistTypeEnum

class ArtistTypeModel(Base):
    __tablename__ = "artist_types"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(SQLAlchemyEnum(ArtistTypeEnum), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Importação tardia para evitar importação circular
from infrastructure.database.models.artist_model import ArtistModel
ArtistTypeModel.artists = relationship("ArtistModel", back_populates="artist_type") 