from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# Schemas relacionados  
from .profile import ProfileResponse
from .space_event_type import SpaceEventTypeResponse
from .space_festival_type import SpaceFestivalTypeResponse

# Enum para status
class StatusInterestEnum(str, Enum):
    AGUARDANDO_CONFIRMACAO = "AGUARDANDO_CONFIRMACAO"
    ACEITO = "ACEITO"
    RECUSADO = "RECUSADO"

class InterestBase(BaseModel):
    profile_id_interessado: int
    profile_id_interesse: int
    data_inicial: date
    horario_inicial: str
    duracao_apresentacao: float
    valor_hora_ofertado: float
    valor_couvert_ofertado: float
    mensagem: str
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None
    resposta: Optional[str] = None
    status: StatusInterestEnum = StatusInterestEnum.AGUARDANDO_CONFIRMACAO

    @field_validator('profile_id_interessado')
    @classmethod
    def validate_profile_id_interessado(cls, v):
        if v <= 0:
            raise ValueError("ID do profile interessado deve ser maior que zero")
        return v

    @field_validator('profile_id_interesse')
    @classmethod
    def validate_profile_id_interesse(cls, v):
        if v <= 0:
            raise ValueError("ID do profile de interesse deve ser maior que zero")
        return v

    @field_validator('horario_inicial')
    @classmethod
    def validate_horario_inicial(cls, v):
        if not v or not v.strip():
            raise ValueError("Horário inicial é obrigatório")
        
        # Validar formato HH:MM
        import re
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v.strip()):
            raise ValueError("Horário inicial deve estar no formato HH:MM")
        
        return v.strip()

    @field_validator('duracao_apresentacao')
    @classmethod
    def validate_duracao_apresentacao(cls, v):
        if v <= 0:
            raise ValueError("Duração da apresentação deve ser um número positivo")
        
        if v > 24:
            raise ValueError("Duração da apresentação não pode exceder 24 horas")
        
        return v

    @field_validator('valor_hora_ofertado')
    @classmethod
    def validate_valor_hora_ofertado(cls, v):
        if v < 0:
            raise ValueError("Valor-hora ofertado deve ser um número não negativo")
        return v

    @field_validator('valor_couvert_ofertado')
    @classmethod
    def validate_valor_couvert_ofertado(cls, v):
        if v < 0:
            raise ValueError("Valor do couvert ofertado deve ser um número não negativo")
        return v

    @field_validator('mensagem')
    @classmethod
    def validate_mensagem(cls, v):
        if not v or not v.strip():
            raise ValueError("Mensagem é obrigatória")
        
        if len(v.strip()) < 10:
            raise ValueError("Mensagem deve ter pelo menos 10 caracteres")
        
        if len(v.strip()) > 1000:
            raise ValueError("Mensagem não pode exceder 1000 caracteres")
        
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

    @field_validator('resposta')
    @classmethod
    def validate_resposta(cls, v):
        if v is not None:
            if len(v.strip()) > 500:
                raise ValueError("Resposta não pode exceder 500 caracteres")
            return v.strip()
        return v

class InterestCreate(InterestBase):
    # Campos que não devem ser definidos na criação
    resposta: Optional[str] = None
    status: StatusInterestEnum = StatusInterestEnum.AGUARDANDO_CONFIRMACAO

class InterestUpdate(BaseModel):
    profile_id_interessado: Optional[int] = None
    profile_id_interesse: Optional[int] = None
    data_inicial: Optional[date] = None
    horario_inicial: Optional[str] = None
    duracao_apresentacao: Optional[float] = None
    valor_hora_ofertado: Optional[float] = None
    valor_couvert_ofertado: Optional[float] = None
    mensagem: Optional[str] = None
    space_event_type_id: Optional[int] = None
    space_festival_type_id: Optional[int] = None
    resposta: Optional[str] = None
    status: Optional[StatusInterestEnum] = None

    @field_validator('profile_id_interessado')
    @classmethod
    def validate_profile_id_interessado(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do profile interessado deve ser maior que zero")
        return v

    @field_validator('profile_id_interesse')
    @classmethod
    def validate_profile_id_interesse(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID do profile de interesse deve ser maior que zero")
        return v

    @field_validator('horario_inicial')
    @classmethod
    def validate_horario_inicial(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Horário inicial é obrigatório")
            
            # Validar formato HH:MM
            import re
            if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v.strip()):
                raise ValueError("Horário inicial deve estar no formato HH:MM")
            
            return v.strip()
        return v

    @field_validator('duracao_apresentacao')
    @classmethod
    def validate_duracao_apresentacao(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Duração da apresentação deve ser um número positivo")
            
            if v > 24:
                raise ValueError("Duração da apresentação não pode exceder 24 horas")
        return v

    @field_validator('valor_hora_ofertado')
    @classmethod
    def validate_valor_hora_ofertado(cls, v):
        if v is not None and v < 0:
            raise ValueError("Valor-hora ofertado deve ser um número não negativo")
        return v

    @field_validator('valor_couvert_ofertado')
    @classmethod
    def validate_valor_couvert_ofertado(cls, v):
        if v is not None and v < 0:
            raise ValueError("Valor do couvert ofertado deve ser um número não negativo")
        return v

    @field_validator('mensagem')
    @classmethod
    def validate_mensagem(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Mensagem é obrigatória")
            
            if len(v.strip()) < 10:
                raise ValueError("Mensagem deve ter pelo menos 10 caracteres")
            
            if len(v.strip()) > 1000:
                raise ValueError("Mensagem não pode exceder 1000 caracteres")
            
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

    @field_validator('resposta')
    @classmethod
    def validate_resposta(cls, v):
        if v is not None:
            if len(v.strip()) > 500:
                raise ValueError("Resposta não pode exceder 500 caracteres")
            return v.strip()
        return v

class InterestResponse(InterestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class InterestWithRelations(InterestResponse):
    """Schema com dados relacionados incluídos"""
    profile_interessado: Optional[ProfileResponse] = None
    profile_interesse: Optional[ProfileResponse] = None
    space_event_type: Optional[SpaceEventTypeResponse] = None
    space_festival_type: Optional[SpaceFestivalTypeResponse] = None

    model_config = {"from_attributes": True}

class InterestListResponse(BaseModel):
    """Schema para resposta de lista de interesses"""
    items: List[InterestResponse]
    
    model_config = {"from_attributes": True}

class InterestListWithRelations(BaseModel):
    """Schema para resposta de lista de interesses com dados relacionados"""
    items: List[InterestWithRelations]
    
    model_config = {"from_attributes": True}

class InterestStatusUpdate(BaseModel):
    """Schema específico para atualização de status"""
    status: StatusInterestEnum
    resposta: Optional[str] = None

    @field_validator('resposta')
    @classmethod
    def validate_resposta(cls, v):
        if v is not None:
            if len(v.strip()) > 500:
                raise ValueError("Resposta não pode exceder 500 caracteres")
            return v.strip()
        return v

class InterestStatistics(BaseModel):
    """Schema para estatísticas de interesse"""
    como_interessado: dict
    como_pessoa_interesse: dict
    total_manifestado: int
    total_recebido: int

    model_config = {"from_attributes": True} 