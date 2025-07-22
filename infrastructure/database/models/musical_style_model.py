from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class MusicalStyleModel(Base):
    __tablename__ = "musical_styles"
    
    id = Column(Integer, primary_key=True, index=True)
    estyle = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<MusicalStyleModel(id={self.id}, estyle='{self.estyle}')>"

# Importação tardia para evitar importação circular
# MusicalStyleModel.artists = relationship("ArtistModel", secondary="artist_musical_style", back_populates="musical_styles") 