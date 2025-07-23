from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from domain.entities.space import AcessoEnum, PublicoEstimadoEnum

# Schemas para relacionamentos
class ProfileRelation(BaseModel):
    id: int
    full_name: str
    artistic_name: str
    bio: str
    cidade: str
    uf: str

    class Config:
        from_attributes = True

class SpaceTypeRelation(BaseModel):
    id: int
    tipo: str

    class Config:
        from_attributes = True

class EventTypeRelation(BaseModel):
    id: int
    type: str

    class Config:
        from_attributes = True

class FestivalTypeRelation(BaseModel):
    id: int
    type: str

    class Config:
        from_attributes = True

class SpaceBase(BaseModel):
    profile_id: int
    space_type_id: int
    event_type_id: Optional[int] = None
    festival_type_id: Optional[int] = None
    acesso: AcessoEnum
    dias_apresentacao: List[str]
    duracao_apresentacao: float
    valor_hora: float
    valor_couvert: float
    requisitos_minimos: str
    oferecimentos: str
    estrutura_apresentacao: str
    publico_estimado: PublicoEstimadoEnum
    fotos_ambiente: List[str]
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None

class SpaceCreate(SpaceBase):
    pass

class SpaceUpdate(BaseModel):
    profile_id: Optional[int] = None
    space_type_id: Optional[int] = None
    event_type_id: Optional[int] = None
    festival_type_id: Optional[int] = None
    acesso: Optional[AcessoEnum] = None
    dias_apresentacao: Optional[List[str]] = None
    duracao_apresentacao: Optional[float] = None
    valor_hora: Optional[float] = None
    valor_couvert: Optional[float] = None
    requisitos_minimos: Optional[str] = None
    oferecimentos: Optional[str] = None
    estrutura_apresentacao: Optional[str] = None
    publico_estimado: Optional[PublicoEstimadoEnum] = None
    fotos_ambiente: Optional[List[str]] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None

class SpaceResponse(SpaceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SpaceResponseWithRelations(SpaceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    profile: Optional[ProfileRelation] = None
    space_type: Optional[SpaceTypeRelation] = None
    event_type: Optional[EventTypeRelation] = None
    festival_type: Optional[FestivalTypeRelation] = None

    class Config:
        from_attributes = True 