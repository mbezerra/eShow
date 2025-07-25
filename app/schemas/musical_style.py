from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MusicalStyleBase(BaseModel):
    estyle: str = Field(..., description="Estilo musical (qualquer valor string)")

class MusicalStyleCreate(MusicalStyleBase):
    pass

class MusicalStyleUpdate(BaseModel):
    estyle: Optional[str] = Field(None, description="Estilo musical (qualquer valor string)")

class MusicalStyleResponse(MusicalStyleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 