from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados
from .profile import ProfileResponse
from .space_event_type import SpaceEventTypeResponse
from .space_festival_type import SpaceFestivalTypeResponse

class ReviewBase(BaseModel):
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None
    data_hora: datetime
    nota: int
    depoimento: str

    @field_validator('nota')
    @classmethod
    def validate_nota(cls, v):
        if not isinstance(v, int) or v < 1 or v > 5:
            raise ValueError("Nota deve ser um número inteiro entre 1 e 5")
        return v

    @field_validator('depoimento')
    @classmethod
    def validate_depoimento(cls, v):
        if not v or not v.strip():
            raise ValueError("Depoimento não pode estar vazio")
        
        if len(v.strip()) < 10:
            raise ValueError("Depoimento deve ter pelo menos 10 caracteres")
        
        if len(v.strip()) > 1000:
            raise ValueError("Depoimento deve ter no máximo 1000 caracteres")
        
        return v.strip()

    @field_validator('space_event_type_id')
    @classmethod
    def validate_space_event_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        return v

    @field_validator('space_festival_type_id')
    @classmethod
    def validate_space_festival_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
        return v

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    nota: Optional[int] = None
    depoimento: Optional[str] = None
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None

    @field_validator('nota')
    @classmethod
    def validate_nota(cls, v):
        if v is not None and (not isinstance(v, int) or v < 1 or v > 5):
            raise ValueError("Nota deve ser um número inteiro entre 1 e 5")
        return v

    @field_validator('depoimento')
    @classmethod
    def validate_depoimento(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Depoimento não pode estar vazio")
            
            if len(v.strip()) < 10:
                raise ValueError("Depoimento deve ter pelo menos 10 caracteres")
            
            if len(v.strip()) > 1000:
                raise ValueError("Depoimento deve ter no máximo 1000 caracteres")
            
            return v.strip()
        return v

    @field_validator('space_event_type_id')
    @classmethod
    def validate_space_event_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        return v

    @field_validator('space_festival_type_id')
    @classmethod
    def validate_space_festival_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
        return v

class ReviewResponse(ReviewBase):
    profile_id: int
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ReviewWithRelations(ReviewResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None
    space_event_type: Optional[SpaceEventTypeResponse] = None
    space_festival_type: Optional[SpaceFestivalTypeResponse] = None

    model_config = {"from_attributes": True}

class ReviewListResponse(BaseModel):
    """Schema para resposta de lista de reviews"""
    items: List[ReviewResponse]

    model_config = {"from_attributes": True}

class ReviewListWithRelations(BaseModel):
    """Schema para resposta de lista de reviews com dados relacionados"""
    items: List[ReviewWithRelations]

    model_config = {"from_attributes": True}

class ProfileAverageRating(BaseModel):
    """Schema para resposta da média de avaliações de um profile"""
    profile_id: int
    average_rating: Optional[float]
    total_reviews: int

    model_config = {"from_attributes": True} 