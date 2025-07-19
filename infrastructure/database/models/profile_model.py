from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base

class ProfileModel(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    artistic_name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=False)
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    telefone_fixo = Column(String(20), nullable=True)
    telefone_movel = Column(String(20), nullable=False)
    whatsapp = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com Role
    role = relationship("RoleModel", back_populates="profiles") 