from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from domain.entities.artist_type import ArtistTypeEnum

class ArtistTypeBase(BaseModel):
    tipo: ArtistTypeEnum = Field(..., description="Tipo de artista (Cantor(a) solo, Dupla, Trio, Banda, Grupo)")

    model_config = {"from_attributes": True}

class ArtistTypeCreate(ArtistTypeBase):
    pass

class ArtistTypeUpdate(BaseModel):
    tipo: Optional[ArtistTypeEnum] = Field(None, description="Tipo de artista (Cantor(a) solo, Dupla, Trio, Banda, Grupo)")

    model_config = {"from_attributes": True}

class ArtistTypeResponse(ArtistTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 