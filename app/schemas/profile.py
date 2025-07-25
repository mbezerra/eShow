from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProfileBase(BaseModel):
    role_id: int = Field(..., description="ID do role associado")
    full_name: str = Field(..., min_length=1, max_length=255, description="Nome completo ou Razão Social")
    artistic_name: str = Field(..., min_length=1, max_length=255, description="Nome artístico ou Nome de Fantasia")
    bio: str = Field(..., min_length=1, description="Bio (apresentação)")
    cep: str = Field(..., min_length=8, max_length=10, description="CEP")
    logradouro: str = Field(..., min_length=1, max_length=255, description="Logradouro")
    numero: str = Field(..., min_length=1, max_length=20, description="Número")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento")
    cidade: str = Field(..., min_length=1, max_length=100, description="Cidade")
    uf: str = Field(..., min_length=2, max_length=2, description="UF")
    telefone_fixo: Optional[str] = Field(None, max_length=20, description="Telefone Fixo")
    telefone_movel: str = Field(..., min_length=1, max_length=20, description="Telefone Móvel")
    whatsapp: Optional[str] = Field(None, max_length=20, description="WhatsApp")

class ProfileCreate(ProfileBase):
    user_id: Optional[int] = Field(None, description="ID do usuário associado")

class ProfileUpdate(BaseModel):
    user_id: Optional[int] = Field(None, description="ID do usuário associado")
    role_id: Optional[int] = Field(None, description="ID do role associado")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome completo ou Razão Social")
    artistic_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome artístico ou Nome de Fantasia")
    bio: Optional[str] = Field(None, min_length=1, description="Bio (apresentação)")
    cep: Optional[str] = Field(None, min_length=8, max_length=10, description="CEP")
    logradouro: Optional[str] = Field(None, min_length=1, max_length=255, description="Logradouro")
    numero: Optional[str] = Field(None, min_length=1, max_length=20, description="Número")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento")
    cidade: Optional[str] = Field(None, min_length=1, max_length=100, description="Cidade")
    uf: Optional[str] = Field(None, min_length=2, max_length=2, description="UF")
    telefone_fixo: Optional[str] = Field(None, max_length=20, description="Telefone Fixo")
    telefone_movel: Optional[str] = Field(None, min_length=1, max_length=20, description="Telefone Móvel")
    whatsapp: Optional[str] = Field(None, max_length=20, description="WhatsApp")

class ProfileResponse(ProfileBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 