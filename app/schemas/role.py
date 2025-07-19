from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain.entities.role import RoleType

class RoleBase(BaseModel):
    role: RoleType = Field(..., description="Tipo do role (Admin, Artista, Espaço)")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    role: Optional[RoleType] = Field(None, description="Tipo do role (Admin, Artista, Espaço)")

class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 