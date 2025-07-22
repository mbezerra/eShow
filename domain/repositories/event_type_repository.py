from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.event_type import EventType

class EventTypeRepository(ABC):
    @abstractmethod
    def create(self, event_type: EventType) -> EventType:
        pass
    
    @abstractmethod
    def get_by_id(self, event_type_id: int) -> Optional[EventType]:
        pass
    
    @abstractmethod
    def get_by_type(self, type: str) -> Optional[EventType]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[EventType]:
        pass
    
    @abstractmethod
    def update(self, event_type: EventType) -> EventType:
        pass
    
    @abstractmethod
    def delete(self, event_type_id: int) -> bool:
        pass 