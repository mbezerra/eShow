from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EventTypeBase(BaseModel):
    type: str

class EventTypeCreate(EventTypeBase):
    pass

class EventTypeUpdate(BaseModel):
    type: str

class EventTypeResponse(EventTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 