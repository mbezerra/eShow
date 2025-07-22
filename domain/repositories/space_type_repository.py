from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.space_type import SpaceType

class SpaceTypeRepository(ABC):
    @abstractmethod
    def create(self, space_type: SpaceType) -> SpaceType:
        pass
    
    @abstractmethod
    def get_by_id(self, space_type_id: int) -> Optional[SpaceType]:
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: str) -> Optional[SpaceType]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpaceType]:
        pass
    
    @abstractmethod
    def update(self, space_type: SpaceType) -> SpaceType:
        pass
    
    @abstractmethod
    def delete(self, space_type_id: int) -> bool:
        pass 