from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados
from .artist import ArtistResponse
from .musical_style import MusicalStyleResponse

class ArtistMusicalStyleBase(BaseModel):
    artist_id: int
    musical_style_id: int

    @field_validator('artist_id')
    @classmethod
    def validate_artist_id(cls, v):
        if v <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        return v

    @field_validator('musical_style_id')
    @classmethod
    def validate_musical_style_id(cls, v):
        if v <= 0:
            raise ValueError("ID do estilo musical deve ser maior que zero")
        return v

class ArtistMusicalStyleCreate(ArtistMusicalStyleBase):
    pass

class ArtistMusicalStyleResponse(ArtistMusicalStyleBase):
    id: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class ArtistMusicalStyleWithRelations(ArtistMusicalStyleResponse):
    """Schema com dados relacionados incluídos"""
    artist: Optional[ArtistResponse] = None
    musical_style: Optional[MusicalStyleResponse] = None

    model_config = {"from_attributes": True}

class ArtistMusicalStyleListResponse(BaseModel):
    """Schema para resposta de lista de relacionamentos"""
    items: List[ArtistMusicalStyleResponse]
    
    model_config = {"from_attributes": True}

class ArtistMusicalStyleListWithRelations(BaseModel):
    """Schema para resposta de lista de relacionamentos com dados relacionados"""
    items: List[ArtistMusicalStyleWithRelations]
    
    model_config = {"from_attributes": True}

class ArtistMusicalStyleBulkCreate(BaseModel):
    """Schema para criação em lote de relacionamentos"""
    artist_id: int
    musical_style_ids: List[int]

    @field_validator('artist_id')
    @classmethod
    def validate_artist_id(cls, v):
        if v <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        return v

    @field_validator('musical_style_ids')
    @classmethod
    def validate_musical_style_ids(cls, v):
        if not v:
            raise ValueError("Lista de IDs de estilos musicais não pode estar vazia")
        if not all(style_id > 0 for style_id in v):
            raise ValueError("Todos os IDs de estilos musicais devem ser maiores que zero")
        return v 