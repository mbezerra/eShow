from pydantic import BaseModel, validator
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

    @validator('profile_id')
    def validate_profile_id(cls, v):
        if v <= 0:
            raise ValueError("ID do profile deve ser maior que zero")
        return v

    @validator('banco')
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

    @validator('agencia')
    def validate_agencia(cls, v):
        if not v or not v.strip():
            raise ValueError("Agência não pode estar vazia")
        
        agencia_clean = v.strip()
        if len(agencia_clean) < 3 or len(agencia_clean) > 10:
            raise ValueError("Agência deve ter entre 3 e 10 caracteres")
        
        return agencia_clean

    @validator('conta')
    def validate_conta(cls, v):
        if not v or not v.strip():
            raise ValueError("Conta não pode estar vazia")
        
        conta_clean = v.strip()
        if len(conta_clean) < 4 or len(conta_clean) > 15:
            raise ValueError("Conta deve ter entre 4 e 15 caracteres")
        
        return conta_clean

    @validator('cpf_cnpj')
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

    @validator('chave_pix')
    def validate_chave_pix(cls, v, values):
        if not v or not v.strip():
            raise ValueError("Chave PIX não pode estar vazia")
        
        chave_clean = v.strip()
        
        if len(chave_clean) > 50:
            raise ValueError("Chave PIX deve ter no máximo 50 caracteres")
        
        # Validações específicas por tipo de chave
        tipo_chave_pix = values.get('tipo_chave_pix')
        
        if tipo_chave_pix == TipoChavePixEnum.CPF:
            cpf_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(cpf_clean) != 11 or not cpf_clean.isdigit():
                raise ValueError("Chave PIX tipo CPF deve ter 11 dígitos")
        
        elif tipo_chave_pix == TipoChavePixEnum.CNPJ:
            cnpj_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(cnpj_clean) != 14 or not cnpj_clean.isdigit():
                raise ValueError("Chave PIX tipo CNPJ deve ter 14 dígitos")
        
        elif tipo_chave_pix == TipoChavePixEnum.CELULAR:
            celular_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(celular_clean) < 10 or len(celular_clean) > 11:
                raise ValueError("Chave PIX tipo Celular deve ter 10 ou 11 dígitos")
        
        elif tipo_chave_pix == TipoChavePixEnum.EMAIL:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, chave_clean):
                raise ValueError("Chave PIX tipo E-mail deve ter formato válido")
        
        elif tipo_chave_pix == TipoChavePixEnum.ALEATORIA:
            if len(chave_clean) < 32 or len(chave_clean) > 36:
                raise ValueError("Chave PIX aleatória deve ter entre 32 e 36 caracteres")
        
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

    @validator('banco')
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

    @validator('agencia')
    def validate_agencia(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Agência não pode estar vazia")
            
            agencia_clean = v.strip()
            if len(agencia_clean) < 3 or len(agencia_clean) > 10:
                raise ValueError("Agência deve ter entre 3 e 10 caracteres")
            
            return agencia_clean
        return v

    @validator('conta')
    def validate_conta(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Conta não pode estar vazia")
            
            conta_clean = v.strip()
            if len(conta_clean) < 4 or len(conta_clean) > 15:
                raise ValueError("Conta deve ter entre 4 e 15 caracteres")
            
            return conta_clean
        return v

    @validator('cpf_cnpj')
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

    @validator('chave_pix')
    def validate_chave_pix(cls, v, values):
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Chave PIX não pode estar vazia")
            
            chave_clean = v.strip()
            
            if len(chave_clean) > 50:
                raise ValueError("Chave PIX deve ter no máximo 50 caracteres")
            
            # Validações específicas por tipo de chave
            tipo_chave_pix = values.get('tipo_chave_pix')
            
            if tipo_chave_pix == TipoChavePixEnum.CPF:
                cpf_clean = re.sub(r'[^\d]', '', chave_clean)
                if len(cpf_clean) != 11 or not cpf_clean.isdigit():
                    raise ValueError("Chave PIX tipo CPF deve ter 11 dígitos")
            
            elif tipo_chave_pix == TipoChavePixEnum.CNPJ:
                cnpj_clean = re.sub(r'[^\d]', '', chave_clean)
                if len(cnpj_clean) != 14 or not cnpj_clean.isdigit():
                    raise ValueError("Chave PIX tipo CNPJ deve ter 14 dígitos")
            
            elif tipo_chave_pix == TipoChavePixEnum.CELULAR:
                celular_clean = re.sub(r'[^\d]', '', chave_clean)
                if len(celular_clean) < 10 or len(celular_clean) > 11:
                    raise ValueError("Chave PIX tipo Celular deve ter 10 ou 11 dígitos")
            
            elif tipo_chave_pix == TipoChavePixEnum.EMAIL:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, chave_clean):
                    raise ValueError("Chave PIX tipo E-mail deve ter formato válido")
            
            elif tipo_chave_pix == TipoChavePixEnum.ALEATORIA:
                if len(chave_clean) < 32 or len(chave_clean) > 36:
                    raise ValueError("Chave PIX aleatória deve ter entre 32 e 36 caracteres")
            
            return chave_clean
        return v

class FinancialResponse(FinancialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FinancialWithRelations(FinancialResponse):
    """Schema com dados relacionados incluídos"""
    profile: Optional[ProfileResponse] = None

class FinancialListResponse(BaseModel):
    """Schema para resposta de lista de financials"""
    items: List[FinancialResponse]
    
    class Config:
        from_attributes = True

class FinancialListWithRelations(BaseModel):
    """Schema para resposta de lista de financials com dados relacionados"""
    items: List[FinancialWithRelations]
    
    class Config:
        from_attributes = True 