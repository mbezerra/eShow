from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from domain.entities.space_festival_type import StatusFestivalType

# Schemas relacionados
from .space import SpaceResponse
from .festival_type import FestivalTypeResponse

class SpaceFestivalTypeBase(BaseModel):
    space_id: int
    festival_type_id: int
    tema: str
    descricao: str
    status: StatusFestivalType = StatusFestivalType.CONTRATANDO
    data: datetime
    horario: str
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner

    @field_validator('space_id')
    @classmethod
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @field_validator('festival_type_id')
    @classmethod
    def validate_festival_type_id(cls, v):
        if v <= 0:
            raise ValueError("ID do tipo de festival deve ser maior que zero")
        return v

    @field_validator('tema')
    @classmethod
    def validate_tema(cls, v):
        if not v or not v.strip():
            raise ValueError("Tema é obrigatório")
        return v.strip()

    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v):
        if not v or not v.strip():
            raise ValueError("Descrição é obrigatória")
        return v.strip()

    @field_validator('horario')
    @classmethod
    def validate_horario(cls, v):
        if not v or not v.strip():
            raise ValueError("Horário é obrigatório")
        return v.strip()

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if not isinstance(v, StatusFestivalType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceFestivalTypeCreate(SpaceFestivalTypeBase):
    pass

class SpaceFestivalTypeUpdate(BaseModel):
    tema: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusFestivalType] = None
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner
    data: Optional[datetime] = None
    horario: Optional[str] = None

    @field_validator('tema')
    @classmethod
    def validate_tema(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Tema não pode estar vazio")
        return v.strip() if v else v

    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Descrição não pode estar vazia")
        return v.strip() if v else v

    @field_validator('horario')
    @classmethod
    def validate_horario(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Horário não pode estar vazio")
        return v.strip() if v else v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and not isinstance(v, StatusFestivalType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceFestivalTypeStatusUpdate(BaseModel):
    """Schema específico para atualização de status"""
    status: StatusFestivalType

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if not isinstance(v, StatusFestivalType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceFestivalTypeResponse(SpaceFestivalTypeBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class SpaceFestivalTypeWithRelations(SpaceFestivalTypeResponse):
    """Schema com dados relacionados incluídos"""
    space: Optional[SpaceResponse] = None
    festival_type: Optional[FestivalTypeResponse] = None

class SpaceFestivalTypeListResponse(BaseModel):
    """Schema para resposta de lista de relacionamentos"""
    items: List[SpaceFestivalTypeResponse]
    
    model_config = {"from_attributes": True}

class SpaceFestivalTypeListWithRelations(BaseModel):
    """Schema para resposta de lista de relacionamentos com dados relacionados"""
    items: List[SpaceFestivalTypeWithRelations]
    
    model_config = {"from_attributes": True}

class SpaceFestivalTypeBulkCreate(BaseModel):
    """Schema para criação em lote de relacionamentos para um espaço"""
    space_id: int
    festivals: List[dict]

    @field_validator('space_id')
    @classmethod
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @field_validator('festivals')
    @classmethod
    def validate_festivals(cls, v):
        if not v:
            raise ValueError("Lista de festivais não pode estar vazia")
        return v 