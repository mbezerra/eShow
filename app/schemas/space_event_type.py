from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from domain.entities.space_event_type import StatusEventType

# Schemas relacionados
from .space import SpaceResponse
from .event_type import EventTypeResponse

class SpaceEventTypeBase(BaseModel):
    space_id: int
    event_type_id: int
    tema: str
    descricao: str
    status: StatusEventType = StatusEventType.CONTRATANDO
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner
    data: datetime
    horario: str

    @validator('space_id')
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('event_type_id')
    def validate_event_type_id(cls, v):
        if v <= 0:
            raise ValueError("ID do tipo de evento deve ser maior que zero")
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

    @validator('status')
    def validate_status(cls, v):
        if not isinstance(v, StatusEventType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceEventTypeCreate(SpaceEventTypeBase):
    pass

class SpaceEventTypeUpdate(BaseModel):
    tema: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusEventType] = None
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

    @validator('status')
    def validate_status(cls, v):
        if v is not None and not isinstance(v, StatusEventType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceEventTypeStatusUpdate(BaseModel):
    """Schema específico para atualização de status"""
    status: StatusEventType

    @validator('status')
    def validate_status(cls, v):
        if not isinstance(v, StatusEventType):
            raise ValueError("Status deve ser um valor válido")
        return v

class SpaceEventTypeResponse(SpaceEventTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SpaceEventTypeWithRelations(SpaceEventTypeResponse):
    """Schema com dados relacionados incluídos"""
    space: Optional[SpaceResponse] = None
    event_type: Optional[EventTypeResponse] = None

class SpaceEventTypeListResponse(BaseModel):
    """Schema para resposta de lista de relacionamentos"""
    items: List[SpaceEventTypeResponse]
    
    class Config:
        from_attributes = True

class SpaceEventTypeListWithRelations(BaseModel):
    """Schema para resposta de lista de relacionamentos com dados relacionados"""
    items: List[SpaceEventTypeWithRelations]
    
    class Config:
        from_attributes = True

class SpaceEventTypeBulkCreate(BaseModel):
    """Schema para criação em lote de relacionamentos para um espaço"""
    space_id: int
    events: List[dict]

    @validator('space_id')
    def validate_space_id(cls, v):
        if v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('events')
    def validate_events(cls, v):
        if not v:
            raise ValueError("Lista de eventos não pode estar vazia")
        return v 