from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import re

# Schemas relacionados
from .profile import ProfileResponse

class TipoContaEnum(str, Enum):
    """Enum para tipos de conta bancária"""
    POUPANCA = "Poupança"
    CORRENTE = "Corrente"

class TipoChavePixEnum(str, Enum):
    """Enum para tipos de chave PIX"""
    CPF = "CPF"
    CNPJ = "CNPJ"
    CELULAR = "Celular"
    EMAIL = "E-mail"
    ALEATORIA = "Aleatória"

class PreferenciaTransferenciaEnum(str, Enum):
    """Enum para preferências de transferência"""
    PIX = "PIX"
    TED = "TED"

class FinancialBase(BaseModel):
    profile_id: int
    banco: str
    agencia: str
    conta: str
    tipo_conta: TipoContaEnum
    cpf_cnpj: str
    tipo_chave_pix: TipoChavePixEnum
    chave_pix: str
    preferencia: PreferenciaTransferenciaEnum

    @field_validator('profile_id')
    @classmethod
    def validate_profile_id(cls, v):
        if v <= 0:
            raise ValueError("ID do profile deve ser maior que zero")
        return v

    @field_validator('banco')
    @classmethod
    def validate_banco(cls, v):
        if not isinstance(v, str):
            raise ValueError("Código do banco deve ser uma string")
        
        if not v.isdigit():
            raise ValueError("Código do banco deve conter apenas dígitos")
        
        if len(v) != 3:
            raise ValueError("Código do banco deve ter exatamente 3 dígitos")
        
        banco_num = int(v)
        if banco_num < 1 or banco_num > 999:
            raise ValueError("Código do banco deve estar entre 001 e 999")
        
        return v

    @field_validator('agencia')
    @classmethod
    def validate_agencia(cls, v):
        if not v or not v.strip():
            raise ValueError("Agência não pode estar vazia")
        
        agencia_clean = v.strip()
        if len(agencia_clean) < 3 or len(agencia_clean) > 10:
            raise ValueError("Agência deve ter entre 3 e 10 caracteres")
        
        return agencia_clean

    @field_validator('conta')
    @classmethod
    def validate_conta(cls, v):
        if not v or not v.strip():
            raise ValueError("Conta não pode estar vazia")
        
        conta_clean = v.strip()
        if len(conta_clean) < 4 or len(conta_clean) > 15:
            raise ValueError("Conta deve ter entre 4 e 15 caracteres")
        
        return conta_clean

    @field_validator('cpf_cnpj')
    @classmethod
    def validate_cpf_cnpj(cls, v):
        if not v or not v.strip():
            raise ValueError("CPF/CNPJ não pode estar vazio")
        
        # Remove caracteres especiais para validação
        cpf_cnpj_clean = re.sub(r'[^\d]', '', v)
        
        if len(cpf_cnpj_clean) == 11:
            # CPF: 11 dígitos
            if not cpf_cnpj_clean.isdigit():
                raise ValueError("CPF deve conter apenas números")
        elif len(cpf_cnpj_clean) == 14:
            # CNPJ: 14 dígitos
            if not cpf_cnpj_clean.isdigit():
                raise ValueError("CNPJ deve conter apenas números")
        else:
            raise ValueError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos")
        
        return v.strip()

    @field_validator('chave_pix')
    @classmethod
    def validate_chave_pix(cls, v):
        if not v or not v.strip():
            raise ValueError("Chave PIX não pode estar vazia")
        
        chave_clean = v.strip()
        
        if len(chave_clean) > 50:
            raise ValueError("Chave PIX deve ter no máximo 50 caracteres")
        
        return chave_clean

class FinancialCreate(FinancialBase):
    pass

class FinancialUpdate(BaseModel):
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    tipo_conta: Optional[TipoContaEnum] = None
    cpf_cnpj: Optional[str] = None
    tipo_chave_pix: Optional[TipoChavePixEnum] = None
    chave_pix: Optional[str] = None
    preferencia: Optional[PreferenciaTransferenciaEnum] = None

    @field_validator('banco')
    @classmethod
    def validate_banco(cls, v):
        if v is not None:
            if not isinstance(v, str):
                raise ValueError("Código do banco deve ser uma string")
            
            if not v.isdigit():
                raise ValueError("Código do banco deve conter apenas dígitos")
            
            if len(v) != 3:
                raise ValueError("Código do banco deve ter exatamente 3 dígitos")
            
            banco_num = int(v)
            if banco_num < 1 or banco_num > 999:
                raise ValueError("Código do banco deve estar entre 001 e 999")
        
        return v

    @field_validator('agencia')
    @classmethod
    def validate_agencia(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Agência não pode estar vazia")
            
            agencia_clean = v.strip()
            if len(agencia_clean) < 3 or len(agencia_clean) > 10:
                raise ValueError("Agência deve ter entre 3 e 10 caracteres")
            
            return agencia_clean
        return v

    @field_validator('conta')
    @classmethod
    def validate_conta(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Conta não pode estar vazia")
            
            conta_clean = v.strip()
            if len(conta_clean) < 4 or len(conta_clean) > 15:
                raise ValueError("Conta deve ter entre 4 e 15 caracteres")
            
            return conta_clean
        return v

    @field_validator('cpf_cnpj')
    @classmethod
    def validate_cpf_cnpj(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("CPF/CNPJ não pode estar vazio")
            
            # Remove caracteres especiais para validação
            cpf_cnpj_clean = re.sub(r'[^\d]', '', v)
            
            if len(cpf_cnpj_clean) == 11:
                # CPF: 11 dígitos
                if not cpf_cnpj_clean.isdigit():
                    raise ValueError("CPF deve conter apenas números")
            elif len(cpf_cnpj_clean) == 14:
                # CNPJ: 14 dígitos
                if not cpf_cnpj_clean.isdigit():
                    raise ValueError("CNPJ deve conter apenas números")
            else:
                raise ValueError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos")
            
            return v.strip()
        return v

    @field_validator('chave_pix')
    @classmethod
    def validate_chave_pix(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Chave PIX não pode estar vazia")
            
            chave_clean = v.strip()
            
            if len(chave_clean) > 50:
                raise ValueError("Chave PIX deve ter no máximo 50 caracteres")
            
            return chave_clean
        return v

class FinancialResponse(FinancialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class FinancialWithRelations(FinancialResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None

class FinancialListResponse(BaseModel):
    """Schema para resposta de lista de financials"""
    items: List[FinancialResponse]
    
    model_config = {"from_attributes": True}

class FinancialListWithRelations(BaseModel):
    """Schema para resposta de lista de financials com dados relacionados"""
    items: List[FinancialWithRelations]
    
    model_config = {"from_attributes": True} 