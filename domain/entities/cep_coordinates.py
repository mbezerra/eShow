from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CepCoordinates:
    """Entidade de domínio para coordenadas de CEPs"""
    
    cep: str
    latitude: float
    longitude: float
    cidade: Optional[str] = None
    uf: Optional[str] = None
    logradouro: Optional[str] = None
    bairro: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações após inicialização"""
        if not self.cep or len(self.cep) != 9:
            raise ValueError("CEP deve ter 9 caracteres (formato: 12345-678)")
        
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude deve estar entre -90 e 90")
        
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude deve estar entre -180 e 180")
    
    @property
    def coordinates(self) -> tuple[float, float]:
        """Retorna as coordenadas como tupla"""
        return (self.latitude, self.longitude)
    
    @property
    def cep_prefix(self) -> str:
        """Retorna o prefixo do CEP (primeiros 5 dígitos)"""
        return self.cep[:5]
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'cep': self.cep,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'cidade': self.cidade,
            'uf': self.uf,
            'logradouro': self.logradouro,
            'bairro': self.bairro,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        } 