from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base
import json

class ArtistModel(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False, unique=True)
    artist_type_id = Column(Integer, ForeignKey("artist_types.id"), nullable=False)
    dias_apresentacao = Column(String, nullable=False)  # JSON string
    raio_atuacao = Column(Float, nullable=False)
    duracao_apresentacao = Column(Float, nullable=False)
    valor_hora = Column(Float, nullable=False)
    valor_couvert = Column(Float, nullable=False)
    requisitos_minimos = Column(String, nullable=False)
    instagram = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    youtube = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    soundcloud = Column(String, nullable=True)
    bandcamp = Column(String, nullable=True)
    spotify = Column(String, nullable=True)
    deezer = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ArtistModel(id={self.id}, profile_id={self.profile_id}, artist_type_id={self.artist_type_id})>"

# Importação tardia para evitar importação circular
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.artist_type_model import ArtistTypeModel
from infrastructure.database.models.musical_style_model import MusicalStyleModel

ArtistModel.profile = relationship("ProfileModel", back_populates="artist")
ArtistModel.artist_type = relationship("ArtistTypeModel", back_populates="artists")
ArtistModel.musical_styles = relationship("MusicalStyleModel", secondary="artist_musical_style", back_populates="artists") 