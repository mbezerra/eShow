from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MusicalStyleBase(BaseModel):
    style: str = Field(..., min_length=1, max_length=100, description="Estilo musical")

    model_config = {"from_attributes": True}

class MusicalStyleCreate(MusicalStyleBase):
    pass

class MusicalStyleUpdate(BaseModel):
    style: Optional[str] = Field(None, min_length=1, max_length=100, description="Estilo musical")

    model_config = {"from_attributes": True}

class MusicalStyleResponse(MusicalStyleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 