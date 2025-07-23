from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class FinancialModel(Base):
    """Modelo para representar dados financeiros/bancários"""
    __tablename__ = "financials"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    banco = Column(Integer, nullable=False)  # Código do banco (1-999)
    agencia = Column(String(10), nullable=False)
    conta = Column(String(15), nullable=False)
    tipo_conta = Column(String(20), nullable=False)  # "Poupança" ou "Corrente"
    cpf_cnpj = Column(String(20), nullable=False)
    tipo_chave_pix = Column(String(20), nullable=False)  # "CPF", "CNPJ", "Celular", "E-mail", "Aleatória"
    chave_pix = Column(String(50), nullable=False)
    preferencia = Column(String(10), nullable=False)  # "PIX" ou "TED"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    profile = relationship("ProfileModel", foreign_keys=[profile_id])

    def __repr__(self):
        return f"<FinancialModel(id={self.id}, profile_id={self.profile_id}, banco={self.banco}, preferencia='{self.preferencia}')>" 