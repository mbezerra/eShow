from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# Schemas relacionados
from .profile import ProfileResponse
from .space_event_type import SpaceEventTypeResponse
from .space_festival_type import SpaceFestivalTypeResponse

class ReviewBase(BaseModel):
    profile_id: int
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None
    data_hora: datetime
    nota: int
    depoimento: str

    @validator('profile_id')
    def validate_profile_id(cls, v):
        if v <= 0:
            raise ValueError("ID do profile deve ser maior que zero")
        return v

    @validator('nota')
    def validate_nota(cls, v):
        if not isinstance(v, int) or v < 1 or v > 5:
            raise ValueError("Nota deve ser um número inteiro entre 1 e 5")
        return v

    @validator('depoimento')
    def validate_depoimento(cls, v):
        if not v or not v.strip():
            raise ValueError("Depoimento não pode estar vazio")
        
        if len(v.strip()) < 10:
            raise ValueError("Depoimento deve ter pelo menos 10 caracteres")
        
        if len(v.strip()) > 1000:
            raise ValueError("Depoimento deve ter no máximo 1000 caracteres")
        
        return v.strip()

    @validator('space_event_type_id')
    def validate_space_event_type_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        return v

    @validator('space_festival_type_id')
    def validate_space_festival_type_id(cls, v, values):
        if v is not None and v <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
        
        # Validar que apenas um relacionamento pode estar definido
        space_event_type_id = values.get('space_event_type_id')
        
        if v is not None and space_event_type_id is not None:
            raise ValueError("Apenas um tipo de relacionamento pode ser especificado por review")
        
        return v

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    nota: Optional[int] = None
    depoimento: Optional[str] = None
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None

    @validator('nota')
    def validate_nota(cls, v):
        if v is not None and (not isinstance(v, int) or v < 1 or v > 5):
            raise ValueError("Nota deve ser um número inteiro entre 1 e 5")
        return v

    @validator('depoimento')
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

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewWithRelations(ReviewResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None
    space_event_type: Optional[SpaceEventTypeResponse] = None
    space_festival_type: Optional[SpaceFestivalTypeResponse] = None

class ReviewListResponse(BaseModel):
    """Schema para resposta de lista de reviews"""
    items: List[ReviewResponse]
    
    class Config:
        from_attributes = True

class ReviewListWithRelations(BaseModel):
    """Schema para resposta de lista de reviews com dados relacionados"""
    items: List[ReviewWithRelations]
    
    class Config:
        from_attributes = True

class ProfileAverageRating(BaseModel):
    """Schema para resposta da média de avaliações de um profile"""
    profile_id: int
    average_rating: Optional[float]
    total_reviews: int
    
    class Config:
        from_attributes = True 