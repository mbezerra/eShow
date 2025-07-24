from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from infrastructure.database.database import Base
from domain.entities.space_festival_type import StatusFestivalType

class SpaceFestivalTypeModel(Base):
    """Modelo para representar o relacionamento N:N entre Spaces e Festival Types"""
    __tablename__ = "space_festival_types"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    festival_type_id = Column(Integer, ForeignKey("festival_types.id"), nullable=False)
    tema = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(SQLAlchemyEnum(StatusFestivalType), nullable=False, default=StatusFestivalType.CONTRATANDO)
    link_divulgacao = Column(String(500), nullable=True)
    banner = Column(String(500), nullable=True)  # Path local da imagem do banner
    data = Column(DateTime(timezone=True), nullable=False)
    horario = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<SpaceFestivalTypeModel(id={self.id}, space_id={self.space_id}, festival_type_id={self.festival_type_id}, tema='{self.tema}', status='{self.status}')>" 