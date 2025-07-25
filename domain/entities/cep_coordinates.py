from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CepCoordinates:
    """Entidade de domínio para coordenadas de municípios"""
    
    cidade: str
    uf: str
    latitude: float
    longitude: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações após inicialização"""
        if not self.cidade or not self.cidade.strip():
            raise ValueError("Cidade é obrigatória")
        
        if not self.uf or len(self.uf) != 2:
            raise ValueError("UF deve ter 2 caracteres")
        
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude deve estar entre -90 e 90")
        
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude deve estar entre -180 e 180")
    
    @property
    def coordinates(self) -> tuple[float, float]:
        """Retorna as coordenadas como tupla"""
        return (self.latitude, self.longitude)
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'cidade': self.cidade,
            'uf': self.uf,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        } 