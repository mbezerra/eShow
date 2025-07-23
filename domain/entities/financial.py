from datetime import datetime
from typing import Optional
from enum import Enum
import re

class TipoConta(Enum):
    """Enum para tipos de conta bancária"""
    POUPANCA = "Poupança"
    CORRENTE = "Corrente"

class TipoChavePix(Enum):
    """Enum para tipos de chave PIX"""
    CPF = "CPF"
    CNPJ = "CNPJ"
    CELULAR = "Celular"
    EMAIL = "E-mail"
    ALEATORIA = "Aleatória"

class PreferenciaTransferencia(Enum):
    """Enum para preferências de transferência"""
    PIX = "PIX"
    TED = "TED"

class Financial:
    """Entidade de domínio para dados financeiros/bancários"""
    
    def __init__(
        self,
        profile_id: int,
        banco: int,
        agencia: str,
        conta: str,
        tipo_conta: TipoConta,
        cpf_cnpj: str,
        tipo_chave_pix: TipoChavePix,
        chave_pix: str,
        preferencia: PreferenciaTransferencia,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.profile_id = profile_id
        self.banco = banco
        self.agencia = agencia
        self.conta = conta
        self.tipo_conta = tipo_conta
        self.cpf_cnpj = cpf_cnpj
        self.tipo_chave_pix = tipo_chave_pix
        self.chave_pix = chave_pix
        self.preferencia = preferencia
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Validações de negócio
        self._validate_profile_id()
        self._validate_banco()
        self._validate_agencia()
        self._validate_conta()
        self._validate_cpf_cnpj()
        self._validate_chave_pix()
    
    def _validate_profile_id(self):
        """Validar se o profile_id é válido"""
        if not isinstance(self.profile_id, int) or self.profile_id <= 0:
            raise ValueError("ID do profile deve ser um número inteiro positivo")
    
    def _validate_banco(self):
        """Validar código do banco (3 dígitos)"""
        if not isinstance(self.banco, int) or self.banco < 1 or self.banco > 999:
            raise ValueError("Código do banco deve ser um número entre 1 e 999")
    
    def _validate_agencia(self):
        """Validar agência bancária"""
        if not self.agencia or not self.agencia.strip():
            raise ValueError("Agência não pode estar vazia")
        
        agencia_clean = self.agencia.strip()
        if len(agencia_clean) < 3 or len(agencia_clean) > 10:
            raise ValueError("Agência deve ter entre 3 e 10 caracteres")
    
    def _validate_conta(self):
        """Validar conta bancária"""
        if not self.conta or not self.conta.strip():
            raise ValueError("Conta não pode estar vazia")
        
        conta_clean = self.conta.strip()
        if len(conta_clean) < 4 or len(conta_clean) > 15:
            raise ValueError("Conta deve ter entre 4 e 15 caracteres")
    
    def _validate_cpf_cnpj(self):
        """Validar formato básico de CPF/CNPJ"""
        if not self.cpf_cnpj or not self.cpf_cnpj.strip():
            raise ValueError("CPF/CNPJ não pode estar vazio")
        
        # Remove caracteres especiais para validação
        cpf_cnpj_clean = re.sub(r'[^\d]', '', self.cpf_cnpj)
        
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
    
    def _validate_chave_pix(self):
        """Validar chave PIX conforme o tipo"""
        if not self.chave_pix or not self.chave_pix.strip():
            raise ValueError("Chave PIX não pode estar vazia")
        
        chave_clean = self.chave_pix.strip()
        
        if len(chave_clean) > 50:
            raise ValueError("Chave PIX deve ter no máximo 50 caracteres")
        
        # Validações específicas por tipo de chave
        if self.tipo_chave_pix == TipoChavePix.CPF:
            cpf_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(cpf_clean) != 11 or not cpf_clean.isdigit():
                raise ValueError("Chave PIX tipo CPF deve ter 11 dígitos")
        
        elif self.tipo_chave_pix == TipoChavePix.CNPJ:
            cnpj_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(cnpj_clean) != 14 or not cnpj_clean.isdigit():
                raise ValueError("Chave PIX tipo CNPJ deve ter 14 dígitos")
        
        elif self.tipo_chave_pix == TipoChavePix.CELULAR:
            celular_clean = re.sub(r'[^\d]', '', chave_clean)
            if len(celular_clean) < 10 or len(celular_clean) > 11:
                raise ValueError("Chave PIX tipo Celular deve ter 10 ou 11 dígitos")
        
        elif self.tipo_chave_pix == TipoChavePix.EMAIL:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, chave_clean):
                raise ValueError("Chave PIX tipo E-mail deve ter formato válido")
        
        elif self.tipo_chave_pix == TipoChavePix.ALEATORIA:
            if len(chave_clean) < 32 or len(chave_clean) > 36:
                raise ValueError("Chave PIX aleatória deve ter entre 32 e 36 caracteres")
    
    def update_banco(self, novo_banco: int):
        """Atualizar código do banco"""
        old_banco = self.banco
        self.banco = novo_banco
        try:
            self._validate_banco()
        except ValueError as e:
            self.banco = old_banco  # Reverter em caso de erro
            raise e
    
    def update_chave_pix(self, nova_chave: str, novo_tipo: Optional[TipoChavePix] = None):
        """Atualizar chave PIX e opcionalmente o tipo"""
        old_chave = self.chave_pix
        old_tipo = self.tipo_chave_pix
        
        self.chave_pix = nova_chave
        if novo_tipo:
            self.tipo_chave_pix = novo_tipo
        
        try:
            self._validate_chave_pix()
        except ValueError as e:
            self.chave_pix = old_chave  # Reverter em caso de erro
            self.tipo_chave_pix = old_tipo
            raise e
    
    def __str__(self):
        return f"Financial(id={self.id}, profile_id={self.profile_id}, banco={self.banco})"
    
    def __repr__(self):
        return (f"Financial(id={self.id}, profile_id={self.profile_id}, "
                f"banco={self.banco}, preferencia={self.preferencia.value})") 