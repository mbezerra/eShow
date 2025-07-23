from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados  
from .profile import ProfileResponse
from .space import SpaceResponse
# from .artist import ArtistResponse  # Evitar imports circulares
from .space_event_type import SpaceEventTypeResponse
from .space_festival_type import SpaceFestivalTypeResponse

# Schema simplificado para artista nos relacionamentos de booking
class ArtistRelation(BaseModel):
    id: int
    profile_id: int
    artist_type_id: int
    dias_apresentacao: List[str]
    raio_atuacao: float
    duracao_apresentacao: float
    valor_hora: float
    valor_couvert: float
    requisitos_minimos: str
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None
    soundcloud: Optional[str] = None
    bandcamp: Optional[str] = None
    spotify: Optional[str] = None
    deezer: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    profile_id: int
    data_inicio: datetime
    horario_inicio: str
    data_fim: datetime
    horario_fim: str
    space_id: Optional[int] = None  # Para agendamento de artista
    artist_id: Optional[int] = None  # Para agendamento de espaço
    space_event_type_id: Optional[int] = None  # Para eventos
    space_festival_type_id: Optional[int] = None  # Para festivais

    @validator('profile_id')
    def validate_profile_id(cls, v):
        if v <= 0:
            raise ValueError("ID do profile deve ser maior que zero")
        return v

    @validator('horario_inicio')
    def validate_horario_inicio(cls, v):
        if not v or not v.strip():
            raise ValueError("Horário de início é obrigatório")
        return v.strip()

    @validator('horario_fim')
    def validate_horario_fim(cls, v):
        if not v or not v.strip():
            raise ValueError("Horário de fim é obrigatório")
        return v.strip()

    @validator('data_fim')
    def validate_data_fim(cls, v, values):
        if 'data_inicio' in values and v < values['data_inicio']:
            raise ValueError("Data de fim deve ser posterior à data de início")
        return v

    @validator('space_id')
    def validate_space_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('artist_id')
    def validate_artist_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        return v

    @validator('space_event_type_id')
    def validate_space_event_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        return v

    @validator('space_festival_type_id')
    def validate_space_festival_type_id(cls, v, values):
        if v is not None and v <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
        
        # Validar que apenas um relacionamento está definido
        related_fields = [
            values.get('space_id'),
            values.get('artist_id'),
            values.get('space_event_type_id'),
            v
        ]
        defined_fields = [field for field in related_fields if field is not None]
        
        if len(defined_fields) == 0:
            raise ValueError("Pelo menos um relacionamento deve ser especificado")
        
        if len(defined_fields) > 1:
            raise ValueError("Apenas um tipo de relacionamento pode ser especificado por booking")
        
        return v

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    data_inicio: Optional[datetime] = None
    horario_inicio: Optional[str] = None
    data_fim: Optional[datetime] = None
    horario_fim: Optional[str] = None
    space_id: Optional[int] = None
    artist_id: Optional[int] = None
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None

    @validator('horario_inicio')
    def validate_horario_inicio(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Horário de início não pode estar vazio")
        return v.strip() if v else v

    @validator('horario_fim')
    def validate_horario_fim(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Horário de fim não pode estar vazio")
        return v.strip() if v else v

    @validator('space_id')
    def validate_space_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        return v

    @validator('artist_id')
    def validate_artist_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        return v

    @validator('space_event_type_id')
    def validate_space_event_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        return v

    @validator('space_festival_type_id')
    def validate_space_festival_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
        return v

class BookingResponse(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingWithRelations(BookingResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None
    space: Optional[SpaceResponse] = None
    artist: Optional[ArtistRelation] = None
    space_event_type: Optional[SpaceEventTypeResponse] = None
    space_festival_type: Optional[SpaceFestivalTypeResponse] = None

class BookingListResponse(BaseModel):
    """Schema para resposta de lista de bookings"""
    items: List[BookingResponse]
    
    class Config:
        from_attributes = True

class BookingListWithRelations(BaseModel):
    """Schema para resposta de lista de bookings com dados relacionados"""
    items: List[BookingWithRelations]
    
    class Config:
        from_attributes = True 