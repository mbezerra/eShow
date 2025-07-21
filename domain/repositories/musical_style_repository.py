from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.musical_style import MusicalStyle

class MusicalStyleRepository(ABC):
    @abstractmethod
    def create(self, musical_style: MusicalStyle) -> MusicalStyle:
        pass
    
    @abstractmethod
    def get_by_id(self, musical_style_id: int) -> Optional[MusicalStyle]:
        pass
    
    @abstractmethod
    def get_by_estyle(self, estyle: str) -> Optional[MusicalStyle]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[MusicalStyle]:
        pass
    
    @abstractmethod
    def update(self, musical_style: MusicalStyle) -> MusicalStyle:
        pass
    
    @abstractmethod
    def delete(self, musical_style_id: int) -> bool:
        pass 