from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class ReviewModel(Base):
    """Modelo para representar avaliações/reviews"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)  # Quem está sendo avaliado
    space_event_type_id = Column(Integer, ForeignKey("space_event_types.id"), nullable=True)  # Review de evento
    space_festival_type_id = Column(Integer, ForeignKey("space_festival_types.id"), nullable=True)  # Review de festival
    data_hora = Column(DateTime(timezone=True), nullable=False)
    nota = Column(Integer, nullable=False)  # 1 a 5
    depoimento = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    profile = relationship("ProfileModel", foreign_keys=[profile_id])
    space_event_type = relationship("SpaceEventTypeModel", foreign_keys=[space_event_type_id])
    space_festival_type = relationship("SpaceFestivalTypeModel", foreign_keys=[space_festival_type_id])

    def __repr__(self):
        return f"<ReviewModel(id={self.id}, profile_id={self.profile_id}, nota={self.nota}, data_hora='{self.data_hora}')>" 