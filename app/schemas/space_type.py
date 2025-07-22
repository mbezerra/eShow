from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SpaceTypeBase(BaseModel):
    tipo: str

class SpaceTypeCreate(SpaceTypeBase):
    pass

class SpaceTypeUpdate(BaseModel):
    tipo: str

class SpaceTypeResponse(SpaceTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 