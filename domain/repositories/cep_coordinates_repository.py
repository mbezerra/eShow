from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.cep_coordinates import CepCoordinates

class CepCoordinatesRepository(ABC):
    """Interface do repositório de coordenadas de municípios"""
    
    @abstractmethod
    def get_by_cidade_uf(self, cidade: str, uf: str) -> Optional[CepCoordinates]:
        """Obtém coordenadas por cidade e UF"""
        pass
    
    @abstractmethod
    def get_by_uf(self, uf: str) -> List[CepCoordinates]:
        """Obtém coordenadas por UF"""
        pass
    
    @abstractmethod
    def create(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Cria novo registro de coordenadas"""
        pass
    
    @abstractmethod
    def update(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Atualiza registro de coordenadas"""
        pass
    
    @abstractmethod
    def delete(self, cidade: str, uf: str) -> bool:
        """Deleta registro de coordenadas"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[CepCoordinates]:
        """Obtém todas as coordenadas"""
        pass
    
    @abstractmethod
    def search_by_cidade(self, cidade: str) -> List[CepCoordinates]:
        """Busca municípios por nome da cidade (parcial)"""
        pass
    
    @abstractmethod
    def get_nearby_cities(self, latitude: float, longitude: float, radius_km: float = 50) -> List[CepCoordinates]:
        """Busca cidades próximas usando fórmula de Haversine"""
        pass 