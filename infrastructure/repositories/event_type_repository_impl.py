from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.event_type import EventType
from domain.repositories.event_type_repository import EventTypeRepository
from infrastructure.database.models.event_type_model import EventTypeModel

class EventTypeRepositoryImpl(EventTypeRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, event_type: EventType) -> EventType:
        db_event_type = EventTypeModel(
            type=event_type.type
        )
        self.db.add(db_event_type)
        self.db.commit()
        self.db.refresh(db_event_type)
        return EventType(
            id=db_event_type.id,
            type=db_event_type.type,
            created_at=db_event_type.created_at,
            updated_at=db_event_type.updated_at
        )
    
    def get_by_id(self, event_type_id: int) -> Optional[EventType]:
        db_event_type = self.db.query(EventTypeModel).filter(EventTypeModel.id == event_type_id).first()
        if db_event_type is None:
            return None
        return EventType(
            id=db_event_type.id,
            type=db_event_type.type,
            created_at=db_event_type.created_at,
            updated_at=db_event_type.updated_at
        )
    
    def get_by_type(self, type: str) -> Optional[EventType]:
        db_event_type = self.db.query(EventTypeModel).filter(EventTypeModel.type == type).first()
        if db_event_type is None:
            return None
        return EventType(
            id=db_event_type.id,
            type=db_event_type.type,
            created_at=db_event_type.created_at,
            updated_at=db_event_type.updated_at
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[EventType]:
        db_event_types = self.db.query(EventTypeModel).offset(skip).limit(limit).all()
        return [
            EventType(
                id=db_event_type.id,
                type=db_event_type.type,
                created_at=db_event_type.created_at,
                updated_at=db_event_type.updated_at
            )
            for db_event_type in db_event_types
        ]
    
    def update(self, event_type: EventType) -> EventType:
        db_event_type = self.db.query(EventTypeModel).filter(EventTypeModel.id == event_type.id).first()
        if db_event_type is None:
            raise ValueError(f"EventType with id {event_type.id} not found")
        
        db_event_type.type = event_type.type
        self.db.commit()
        self.db.refresh(db_event_type)
        
        return EventType(
            id=db_event_type.id,
            type=db_event_type.type,
            created_at=db_event_type.created_at,
            updated_at=db_event_type.updated_at
        )
    
    def delete(self, event_type_id: int) -> bool:
        db_event_type = self.db.query(EventTypeModel).filter(EventTypeModel.id == event_type_id).first()
        if db_event_type is None:
            return False
        
        self.db.delete(db_event_type)
        self.db.commit()
        return True 