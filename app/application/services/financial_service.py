from typing import List, Optional, Union, Any
from sqlalchemy.orm import Session
from domain.entities.financial import Financial, TipoConta, TipoChavePix, PreferenciaTransferencia
from domain.repositories.financial_repository import FinancialRepository
from infrastructure.repositories.financial_repository_impl import FinancialRepositoryImpl
from app.schemas.financial import FinancialCreate, FinancialUpdate, TipoContaEnum, TipoChavePixEnum, PreferenciaTransferenciaEnum

class FinancialService:
    """Serviço de aplicação para dados financeiros/bancários"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository: FinancialRepository = FinancialRepositoryImpl(db)
    
    def create_financial(self, financial_data: FinancialCreate) -> Financial:
        """Criar um novo registro financeiro"""
        financial = Financial(
            profile_id=financial_data.profile_id,
            banco=financial_data.banco,
            agencia=financial_data.agencia,
            conta=financial_data.conta,
            tipo_conta=TipoConta(financial_data.tipo_conta.value),
            cpf_cnpj=financial_data.cpf_cnpj,
            tipo_chave_pix=TipoChavePix(financial_data.tipo_chave_pix.value),
            chave_pix=financial_data.chave_pix,
            preferencia=PreferenciaTransferencia(financial_data.preferencia.value)
        )
        
        return self.repository.create(financial)
    
    def get_financial_by_id(self, financial_id: int, include_relations: bool = False) -> Optional[Union[Financial, Any]]:
        """Obter um registro financeiro por ID"""
        return self.repository.get_by_id(financial_id, include_relations)
    
    def get_financials_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros de um profile"""
        return self.repository.get_by_profile_id(profile_id, include_relations)
    
    def get_financials_by_banco(self, banco: int, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros de um banco específico"""
        return self.repository.get_by_banco(banco, include_relations)
    
    def get_financials_by_tipo_conta(self, tipo_conta: TipoContaEnum, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por tipo de conta"""
        return self.repository.get_by_tipo_conta(TipoConta(tipo_conta.value), include_relations)
    
    def get_financials_by_tipo_chave_pix(self, tipo_chave_pix: TipoChavePixEnum, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por tipo de chave PIX"""
        return self.repository.get_by_tipo_chave_pix(TipoChavePix(tipo_chave_pix.value), include_relations)
    
    def get_financial_by_chave_pix(self, chave_pix: str, include_relations: bool = False) -> Optional[Union[Financial, Any]]:
        """Obter registro financeiro por chave PIX"""
        return self.repository.get_by_chave_pix(chave_pix, include_relations)
    
    def get_financials_by_preferencia(self, preferencia: PreferenciaTransferenciaEnum, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por preferência de transferência"""
        return self.repository.get_by_preferencia(PreferenciaTransferencia(preferencia.value), include_relations)
    
    def get_financials_by_cpf_cnpj(self, cpf_cnpj: str, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por CPF/CNPJ"""
        return self.repository.get_by_cpf_cnpj(cpf_cnpj, include_relations)
    
    def update_financial(self, financial_id: int, financial_data: FinancialUpdate) -> Optional[Financial]:
        """Atualizar um registro financeiro"""
        # Primeiro verificar se o registro existe
        existing_financial = self.repository.get_by_id(financial_id)
        if not existing_financial:
            return None
        
        # Criar entidade com os dados atualizados
        updated_financial = Financial(
            profile_id=existing_financial.profile_id,  # Profile não pode ser alterado
            banco=financial_data.banco if financial_data.banco is not None else existing_financial.banco,
            agencia=financial_data.agencia if financial_data.agencia is not None else existing_financial.agencia,
            conta=financial_data.conta if financial_data.conta is not None else existing_financial.conta,
            tipo_conta=TipoConta(financial_data.tipo_conta.value) if financial_data.tipo_conta is not None else existing_financial.tipo_conta,
            cpf_cnpj=financial_data.cpf_cnpj if financial_data.cpf_cnpj is not None else existing_financial.cpf_cnpj,
            tipo_chave_pix=TipoChavePix(financial_data.tipo_chave_pix.value) if financial_data.tipo_chave_pix is not None else existing_financial.tipo_chave_pix,
            chave_pix=financial_data.chave_pix if financial_data.chave_pix is not None else existing_financial.chave_pix,
            preferencia=PreferenciaTransferencia(financial_data.preferencia.value) if financial_data.preferencia is not None else existing_financial.preferencia
        )
        
        return self.repository.update(financial_id, updated_financial)
    
    def delete_financial(self, financial_id: int) -> bool:
        """Deletar um registro financeiro"""
        return self.repository.delete(financial_id)
    
    def get_all_financials(self, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros"""
        return self.repository.get_all(include_relations)
    
    def check_chave_pix_available(self, chave_pix: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar se uma chave PIX está disponível"""
        return not self.repository.check_chave_pix_exists(chave_pix, exclude_id)
    
    def validate_business_rules(self, financial_data: FinancialCreate) -> List[str]:
        """Validar regras de negócio específicas"""
        errors = []
        
        # Verificar se a chave PIX já existe
        if self.repository.check_chave_pix_exists(financial_data.chave_pix):
            errors.append(f"Chave PIX '{financial_data.chave_pix}' já está em uso")
        
        # Validar consistência entre tipo de chave PIX e chave PIX
        tipo_chave = financial_data.tipo_chave_pix
        chave = financial_data.chave_pix
        
        try:
            # Usar as validações da entidade para verificar consistência
            temp_financial = Financial(
                profile_id=financial_data.profile_id,
                banco=financial_data.banco,
                agencia=financial_data.agencia,
                conta=financial_data.conta,
                tipo_conta=TipoConta(financial_data.tipo_conta.value),
                cpf_cnpj=financial_data.cpf_cnpj,
                tipo_chave_pix=TipoChavePix(tipo_chave.value),
                chave_pix=chave,
                preferencia=PreferenciaTransferencia(financial_data.preferencia.value)
            )
        except ValueError as e:
            errors.append(str(e))
        
        return errors
    
    def get_banks_summary(self) -> dict:
        """Obter resumo de registros por banco"""
        all_financials = self.repository.get_all()
        banks_count = {}
        
        for financial in all_financials:
            banco = financial.banco
            if banco in banks_count:
                banks_count[banco] += 1
            else:
                banks_count[banco] = 1
        
        return banks_count
    
    def get_pix_types_summary(self) -> dict:
        """Obter resumo de tipos de chave PIX"""
        all_financials = self.repository.get_all()
        pix_types_count = {}
        
        for financial in all_financials:
            tipo_pix = financial.tipo_chave_pix.value
            if tipo_pix in pix_types_count:
                pix_types_count[tipo_pix] += 1
            else:
                pix_types_count[tipo_pix] = 1
        
        return pix_types_count 