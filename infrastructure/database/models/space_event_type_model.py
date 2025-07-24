from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from infrastructure.database.database import Base
from domain.entities.space_event_type import StatusEventType

class SpaceEventTypeModel(Base):
    """Modelo para representar o relacionamento N:N entre Spaces e Event Types"""
    __tablename__ = "space_event_types"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    event_type_id = Column(Integer, ForeignKey("event_types.id"), nullable=False)
    tema = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(SQLAlchemyEnum(StatusEventType), nullable=False, default=StatusEventType.CONTRATANDO)
    link_divulgacao = Column(String(500), nullable=True)
    banner = Column(String(500), nullable=True)  # Path local da imagem do banner
    data = Column(DateTime(timezone=True), nullable=False)
    horario = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<SpaceEventTypeModel(id={self.id}, space_id={self.space_id}, event_type_id={self.event_type_id}, tema='{self.tema}', status='{self.status}')>" 