from typing import List, Optional
from domain.entities.event_type import EventType
from domain.repositories.event_type_repository import EventTypeRepository

class EventTypeService:
    def __init__(self, event_type_repository: EventTypeRepository):
        self.event_type_repository = event_type_repository
    
    def create_event_type(self, type: str) -> EventType:
        # Verificar se já existe um event type com este type
        existing_event_type = self.event_type_repository.get_by_type(type)
        if existing_event_type:
            raise ValueError(f"EventType with type '{type}' already exists")
        
        event_type = EventType(type=type)
        return self.event_type_repository.create(event_type)
    
    def get_event_type_by_id(self, event_type_id: int) -> Optional[EventType]:
        return self.event_type_repository.get_by_id(event_type_id)
    
    def get_event_type_by_type(self, type: str) -> Optional[EventType]:
        return self.event_type_repository.get_by_type(type)
    
    def get_all_event_types(self, skip: int = 0, limit: int = 100) -> List[EventType]:
        return self.event_type_repository.get_all(skip=skip, limit=limit)
    
    def update_event_type(self, event_type_id: int, type: str) -> EventType:
        event_type = self.event_type_repository.get_by_id(event_type_id)
        if not event_type:
            raise ValueError(f"EventType with id {event_type_id} not found")
        
        # Verificar se já existe outro event type com este type
        existing_event_type = self.event_type_repository.get_by_type(type)
        if existing_event_type and existing_event_type.id != event_type_id:
            raise ValueError(f"EventType with type '{type}' already exists")
        
        event_type.type = type
        return self.event_type_repository.update(event_type)
    
    def delete_event_type(self, event_type_id: int) -> bool:
        return self.event_type_repository.delete(event_type_id) 