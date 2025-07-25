from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FestivalTypeBase(BaseModel):
    type: str

class FestivalTypeCreate(FestivalTypeBase):
    pass

class FestivalTypeUpdate(BaseModel):
    type: str

class FestivalTypeResponse(FestivalTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 