from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados
from .space import SpaceResponse
from .festival_type import FestivalTypeResponse

class SpaceFestivalTypeBase(BaseModel):
    space_id: int
    festival_type_id: int
    tema: str
    descricao: str
    data: datetime
    horario: str
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner

    @validator('space_id')
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('festival_type_id')
    def validate_festival_type_id(cls, v):
        if v <= 0:
            raise ValueError("ID do tipo de festival deve ser maior que zero")
        return v

    @validator('tema')
    def validate_tema(cls, v):
        if not v or not v.strip():
            raise ValueError("Tema é obrigatório")
        return v.strip()

    @validator('descricao')
    def validate_descricao(cls, v):
        if not v or not v.strip():
            raise ValueError("Descrição é obrigatória")
        return v.strip()

    @validator('horario')
    def validate_horario(cls, v):
        if not v or not v.strip():
            raise ValueError("Horário é obrigatório")
        return v.strip()

class SpaceFestivalTypeCreate(SpaceFestivalTypeBase):
    pass

class SpaceFestivalTypeUpdate(BaseModel):
    tema: Optional[str] = None
    descricao: Optional[str] = None
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner
    data: Optional[datetime] = None
    horario: Optional[str] = None

    @validator('tema')
    def validate_tema(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Tema não pode estar vazio")
        return v.strip() if v else v

    @validator('descricao')
    def validate_descricao(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Descrição não pode estar vazia")
        return v.strip() if v else v

    @validator('horario')
    def validate_horario(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Horário não pode estar vazio")
        return v.strip() if v else v

class SpaceFestivalTypeResponse(SpaceFestivalTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SpaceFestivalTypeWithRelations(SpaceFestivalTypeResponse):
    """Schema com dados relacionados incluídos"""
    space: Optional[SpaceResponse] = None
    festival_type: Optional[FestivalTypeResponse] = None

class SpaceFestivalTypeListResponse(BaseModel):
    """Schema para resposta de lista de relacionamentos"""
    items: List[SpaceFestivalTypeResponse]
    
    class Config:
        from_attributes = True

class SpaceFestivalTypeListWithRelations(BaseModel):
    """Schema para resposta de lista de relacionamentos com dados relacionados"""
    items: List[SpaceFestivalTypeWithRelations]
    
    class Config:
        from_attributes = True

class SpaceFestivalTypeBulkCreate(BaseModel):
    """Schema para criação em lote de relacionamentos para um espaço"""
    space_id: int
    festivals: List[dict]

    @validator('space_id')
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('festivals')
    def validate_festivals(cls, v):
        if not v:
            raise ValueError("Lista de festivais não pode estar vazia")
        return v 