from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Nome do role")

    model_config = {"from_attributes": True}

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Nome do role")

    model_config = {"from_attributes": True}

class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 