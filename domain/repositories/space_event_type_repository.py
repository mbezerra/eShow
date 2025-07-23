from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.space_event_type import SpaceEventType

class SpaceEventTypeRepository(ABC):
    """Interface do repositório para o relacionamento N:N entre Spaces e Event Types"""
    
    @abstractmethod
    def create(self, space_event_type: SpaceEventType) -> SpaceEventType:
        """Criar um novo relacionamento entre espaço e tipo de evento"""
        pass
    
    @abstractmethod
    def get_by_id(self, space_event_type_id: int) -> Optional[SpaceEventType]:
        """Obter um relacionamento por ID"""
        pass
    
    @abstractmethod
    def get_by_space_id(self, space_id: int) -> List[SpaceEventType]:
        """Obter todos os tipos de eventos de um espaço"""
        pass
    
    @abstractmethod
    def get_by_event_type_id(self, event_type_id: int) -> List[SpaceEventType]:
        """Obter todos os espaços de um tipo de evento"""
        pass
    
    @abstractmethod
    def get_by_space_and_event_type(self, space_id: int, event_type_id: int) -> List[SpaceEventType]:
        """Obter relacionamentos específicos entre espaço e tipo de evento"""
        pass
    
    @abstractmethod
    def update(self, space_event_type_id: int, space_event_type: SpaceEventType) -> Optional[SpaceEventType]:
        """Atualizar um relacionamento"""
        pass
    
    @abstractmethod
    def delete(self, space_event_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        pass
    
    @abstractmethod
    def delete_by_space_id(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        pass
    
    @abstractmethod
    def delete_by_event_type_id(self, event_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de evento"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[SpaceEventType]:
        """Obter todos os relacionamentos"""
        pass 