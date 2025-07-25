from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados
from .profile import ProfileResponse
from .artist_type import ArtistTypeResponse
from .musical_style import MusicalStyleResponse

class ArtistBase(BaseModel):
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

    @field_validator('dias_apresentacao')
    @classmethod
    def validate_dias_apresentacao(cls, v):
        dias_validos = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        if not v:
            raise ValueError("Dias de apresentação não podem estar vazios")
        if not all(dia in dias_validos for dia in v):
            raise ValueError("Dias de apresentação inválidos")
        return v

    @field_validator('raio_atuacao')
    @classmethod
    def validate_raio_atuacao(cls, v):
        if v <= 0:
            raise ValueError("Raio de atuação deve ser maior que zero")
        return v

    @field_validator('duracao_apresentacao')
    @classmethod
    def validate_duracao_apresentacao(cls, v):
        if v <= 0:
            raise ValueError("Duração da apresentação deve ser maior que zero")
        return v

    @field_validator('valor_hora')
    @classmethod
    def validate_valor_hora(cls, v):
        if v < 0:
            raise ValueError("Valor por hora não pode ser negativo")
        return v

    @field_validator('valor_couvert')
    @classmethod
    def validate_valor_couvert(cls, v):
        if v < 0:
            raise ValueError("Valor do couvert não pode ser negativo")
        return v

    @field_validator('requisitos_minimos')
    @classmethod
    def validate_requisitos_minimos(cls, v):
        if not v or not v.strip():
            raise ValueError("Requisitos mínimos não podem estar vazios")
        return v.strip()

class ArtistCreate(ArtistBase):
    pass

class ArtistUpdate(BaseModel):
    profile_id: Optional[int] = None
    artist_type_id: Optional[int] = None
    dias_apresentacao: Optional[List[str]] = None
    raio_atuacao: Optional[float] = None
    duracao_apresentacao: Optional[float] = None
    valor_hora: Optional[float] = None
    valor_couvert: Optional[float] = None
    requisitos_minimos: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None
    soundcloud: Optional[str] = None
    bandcamp: Optional[str] = None
    spotify: Optional[str] = None
    deezer: Optional[str] = None

    @field_validator('dias_apresentacao')
    @classmethod
    def validate_dias_apresentacao(cls, v):
        if v is not None:
            dias_validos = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
            if not v:
                raise ValueError("Dias de apresentação não podem estar vazios")
            if not all(dia in dias_validos for dia in v):
                raise ValueError("Dias de apresentação inválidos")
        return v

    @field_validator('raio_atuacao')
    @classmethod
    def validate_raio_atuacao(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Raio de atuação deve ser maior que zero")
        return v

    @field_validator('duracao_apresentacao')
    @classmethod
    def validate_duracao_apresentacao(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Duração da apresentação deve ser maior que zero")
        return v

    @field_validator('valor_hora')
    @classmethod
    def validate_valor_hora(cls, v):
        if v is not None and v < 0:
            raise ValueError("Valor por hora não pode ser negativo")
        return v

    @field_validator('valor_couvert')
    @classmethod
    def validate_valor_couvert(cls, v):
        if v is not None and v < 0:
            raise ValueError("Valor do couvert não pode ser negativo")
        return v

    @field_validator('requisitos_minimos')
    @classmethod
    def validate_requisitos_minimos(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Requisitos mínimos não podem estar vazios")
        return v.strip() if v else v

class ArtistResponse(ArtistBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ArtistResponseWithRelations(ArtistResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None
    artist_type: Optional[ArtistTypeResponse] = None
    musical_styles: Optional[List[MusicalStyleResponse]] = None

class ArtistListResponse(BaseModel):
    """Schema para resposta dinâmica de lista de artistas"""
    items: List[ArtistResponse]
    
    model_config = {"from_attributes": True}

class ArtistListResponseWithRelations(BaseModel):
    """Schema para resposta dinâmica de lista de artistas com relacionamentos"""
    items: List[ArtistResponseWithRelations]
    
    model_config = {"from_attributes": True} 