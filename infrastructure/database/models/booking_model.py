from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class BookingModel(Base):
    """Modelo para representar agendamentos/reservas"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    data_inicio = Column(DateTime(timezone=True), nullable=False)
    horario_inicio = Column(String(50), nullable=False)
    data_fim = Column(DateTime(timezone=True), nullable=False)
    horario_fim = Column(String(50), nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=True)  # Para agendamento de artista
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=True)  # Para agendamento de espaço
    space_event_type_id = Column(Integer, ForeignKey("space_event_types.id"), nullable=True)  # Para eventos
    space_festival_type_id = Column(Integer, ForeignKey("space_festival_types.id"), nullable=True)  # Para festivais
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    profile = relationship("ProfileModel", foreign_keys=[profile_id])
    space = relationship("SpaceModel", foreign_keys=[space_id])
    artist = relationship("ArtistModel", foreign_keys=[artist_id])
    space_event_type = relationship("SpaceEventTypeModel", foreign_keys=[space_event_type_id])
    space_festival_type = relationship("SpaceFestivalTypeModel", foreign_keys=[space_festival_type_id])

    def __repr__(self):
        return f"<BookingModel(id={self.id}, profile_id={self.profile_id}, data_inicio='{self.data_inicio}', data_fim='{self.data_fim}')>" 