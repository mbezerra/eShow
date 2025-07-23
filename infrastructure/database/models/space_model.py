from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class SpaceModel(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    space_type_id = Column(Integer, ForeignKey("space_types.id"), nullable=False)
    event_type_id = Column(Integer, ForeignKey("event_types.id"), nullable=True)
    festival_type_id = Column(Integer, ForeignKey("festival_types.id"), nullable=True)
    acesso = Column(String, nullable=False)  # Público, Privado
    dias_apresentacao = Column(JSON, nullable=False)  # Array de strings
    duracao_apresentacao = Column(Float, nullable=False)  # Horas
    valor_hora = Column(Float, nullable=False)  # Reais
    valor_couvert = Column(Float, nullable=False)  # Reais
    requisitos_minimos = Column(Text, nullable=False)
    oferecimentos = Column(Text, nullable=False)
    estrutura_apresentacao = Column(Text, nullable=False)
    publico_estimado = Column(String, nullable=False)  # Enum de faixas
    fotos_ambiente = Column(JSON, nullable=False)  # Array de paths
    instagram = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    youtube = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos serão definidos após a importação dos modelos

# Importação tardia para evitar importação circular
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_type_model import SpaceTypeModel
from infrastructure.database.models.event_type_model import EventTypeModel
from infrastructure.database.models.festival_type_model import FestivalTypeModel

SpaceModel.profile = relationship("ProfileModel", back_populates="spaces")
SpaceModel.space_type = relationship("SpaceTypeModel")
SpaceModel.event_type = relationship("EventTypeModel")
SpaceModel.festival_type = relationship("FestivalTypeModel") 