from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.database import Base
from domain.entities.interest import StatusInterest

class InterestModel(Base):
    """Modelo para representar manifestações de interesse entre profiles"""
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    profile_id_interessado = Column(Integer, ForeignKey("profiles.id"), nullable=False, index=True)
    profile_id_interesse = Column(Integer, ForeignKey("profiles.id"), nullable=False, index=True)
    data_inicial = Column(Date, nullable=False)
    horario_inicial = Column(String(5), nullable=False)  # HH:MM
    duracao_apresentacao = Column(Float, nullable=False)
    valor_hora_ofertado = Column(Float, nullable=False)
    valor_couvert_ofertado = Column(Float, nullable=False)
    space_event_type_id = Column(Integer, ForeignKey("space_event_types.id"), nullable=True)
    space_festival_type_id = Column(Integer, ForeignKey("space_festival_types.id"), nullable=True)
    mensagem = Column(Text, nullable=False)
    resposta = Column(Text, nullable=True)
    status = Column(SQLEnum(StatusInterest), nullable=False, default=StatusInterest.AGUARDANDO_CONFIRMACAO, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    profile_interessado = relationship("ProfileModel", foreign_keys=[profile_id_interessado])
    profile_interesse = relationship("ProfileModel", foreign_keys=[profile_id_interesse])
    space_event_type = relationship("SpaceEventTypeModel", foreign_keys=[space_event_type_id])
    space_festival_type = relationship("SpaceFestivalTypeModel", foreign_keys=[space_festival_type_id])

    def __repr__(self):
        return (f"<InterestModel(id={self.id}, interessado={self.profile_id_interessado}, "
                f"interesse={self.profile_id_interesse}, status='{self.status}')>") 