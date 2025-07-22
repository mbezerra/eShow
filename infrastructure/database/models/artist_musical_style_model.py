from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class ArtistMusicalStyleModel(Base):
    """Modelo para representar o relacionamento N:N entre Artists e Musical Styles"""
    __tablename__ = "artist_musical_style"

    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)
    musical_style_id = Column(Integer, ForeignKey("musical_styles.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ArtistMusicalStyleModel(artist_id={self.artist_id}, musical_style_id={self.musical_style_id})>" 