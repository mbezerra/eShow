from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.space_festival_type import SpaceFestivalType, StatusFestivalType

class SpaceFestivalTypeRepository(ABC):
    """Interface do repositório para o relacionamento N:N entre Spaces e Festival Types"""
    
    @abstractmethod
    def create(self, space_festival_type: SpaceFestivalType) -> SpaceFestivalType:
        """Criar um novo relacionamento entre espaço e tipo de festival"""
        pass
    
    @abstractmethod
    def get_by_id(self, space_festival_type_id: int) -> Optional[SpaceFestivalType]:
        """Obter um relacionamento por ID"""
        pass
    
    @abstractmethod
    def get_by_space_id(self, space_id: int) -> List[SpaceFestivalType]:
        """Obter todos os tipos de festivais de um espaço"""
        pass
    
    @abstractmethod
    def get_by_festival_type_id(self, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter todos os espaços de um tipo de festival"""
        pass
    
    @abstractmethod
    def get_by_space_and_festival_type(self, space_id: int, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter relacionamentos específicos entre espaço e tipo de festival"""
        pass
    
    @abstractmethod
    def update(self, space_festival_type_id: int, space_festival_type: SpaceFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar um relacionamento"""
        pass
    
    @abstractmethod
    def update_status(self, space_festival_type_id: int, status: StatusFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar apenas o status de um relacionamento"""
        pass
    
    @abstractmethod
    def delete(self, space_festival_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        pass
    
    @abstractmethod
    def delete_by_space_id(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        pass
    
    @abstractmethod
    def delete_by_festival_type_id(self, festival_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de festival"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[SpaceFestivalType]:
        """Obter todos os relacionamentos"""
        pass 