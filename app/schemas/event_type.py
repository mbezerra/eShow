from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EventTypeBase(BaseModel):
    type: str = Field(..., min_length=1, max_length=100, description="Tipo de evento")

    model_config = {"from_attributes": True}

class EventTypeCreate(EventTypeBase):
    pass

class EventTypeUpdate(BaseModel):
    type: Optional[str] = Field(None, min_length=1, max_length=100, description="Tipo de evento")

    model_config = {"from_attributes": True}

class EventTypeResponse(EventTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True} 