from sqlalchemy import Column, String, Float, DateTime, Index
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class CepCoordinatesModel(Base):
    """Modelo para armazenar coordenadas de CEPs"""
    
    __tablename__ = "cep_coordinates"
    
    # CEP no formato 12345-678
    cep = Column(String(9), primary_key=True, index=True)
    
    # Coordenadas geográficas
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Informações adicionais
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    logradouro = Column(String(200), nullable=True)
    bairro = Column(String(100), nullable=True)
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Índices para melhor performance
    __table_args__ = (
        Index('idx_cep_coordinates_cidade_uf', 'cidade', 'uf'),
        Index('idx_cep_coordinates_lat_lng', 'latitude', 'longitude'),
    ) 