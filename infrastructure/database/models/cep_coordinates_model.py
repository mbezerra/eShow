from sqlalchemy import Column, String, Float, DateTime, Index, PrimaryKeyConstraint
from sqlalchemy.sql import func
from infrastructure.database.database import Base

class CepCoordinatesModel(Base):
    """Modelo para armazenar coordenadas de municípios"""
    
    __tablename__ = "cep_coordinates"
    
    # Chave primária composta: cidade + uf
    cidade = Column(String(100), nullable=False, primary_key=True)
    uf = Column(String(2), nullable=False, primary_key=True)
    
    # Coluna normalizada para busca sem acentos
    cidade_normalizada = Column(String(100), nullable=False)
    
    # Coordenadas geográficas
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Índices para melhor performance
    __table_args__ = (
        Index('idx_cep_coordinates_lat_lng', 'latitude', 'longitude'),
        Index('idx_cep_coordinates_cidade_normalizada', 'cidade_normalizada'),
    ) 