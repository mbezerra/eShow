from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from domain.entities.cep_coordinates import CepCoordinates

class CepCoordinatesRepository(ABC):
    """Interface para repositório de coordenadas de CEPs"""
    
    @abstractmethod
    def get_by_cep(self, cep: str) -> Optional[CepCoordinates]:
        """Obtém coordenadas por CEP"""
        pass
    
    @abstractmethod
    def get_by_cidade_uf(self, cidade: str, uf: str) -> List[CepCoordinates]:
        """Obtém coordenadas por cidade e UF"""
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
    def delete(self, cep: str) -> bool:
        """Deleta registro de coordenadas"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[CepCoordinates]:
        """Obtém todas as coordenadas"""
        pass
    
    @abstractmethod
    def search_by_prefix(self, cep_prefix: str) -> List[CepCoordinates]:
        """Busca CEPs por prefixo (ex: 48100 para todos os CEPs de Cícero Dantas)"""
        pass 