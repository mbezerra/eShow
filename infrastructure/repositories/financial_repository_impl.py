from typing import List, Optional, Union
from sqlalchemy.orm import Session, joinedload
from domain.repositories.financial_repository import FinancialRepository
from domain.entities.financial import Financial, TipoConta, TipoChavePix, PreferenciaTransferencia
from infrastructure.database.models.financial_model import FinancialModel
from infrastructure.database.models.profile_model import ProfileModel

class FinancialRepositoryImpl(FinancialRepository):
    """Implementação do repositório para dados financeiros/bancários"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _configure_relations(self, query, include_relations: bool = False):
        """Configurar relacionamentos para a query"""
        if include_relations:
            query = query.options(
                joinedload(FinancialModel.profile)
            )
        return query
    
    def create(self, financial: Financial) -> Financial:
        """Criar um novo registro financeiro"""
        # Verificar se o profile existe
        profile = self.db.query(ProfileModel).filter(ProfileModel.id == financial.profile_id).first()
        if not profile:
            raise ValueError(f"Profile com ID {financial.profile_id} não encontrado")
        
        # Verificar se a chave PIX já existe
        if self.check_chave_pix_exists(financial.chave_pix):
            raise ValueError(f"Chave PIX '{financial.chave_pix}' já está em uso")
        
        # Criar o registro financeiro
        db_financial = FinancialModel(
            profile_id=financial.profile_id,
            banco=financial.banco,
            agencia=financial.agencia,
            conta=financial.conta,
            tipo_conta=financial.tipo_conta.value,
            cpf_cnpj=financial.cpf_cnpj,
            tipo_chave_pix=financial.tipo_chave_pix.value,
            chave_pix=financial.chave_pix,
            preferencia=financial.preferencia.value
        )
        
        self.db.add(db_financial)
        self.db.commit()
        self.db.refresh(db_financial)
        
        return self._to_entity(db_financial)
    
    def get_by_id(self, financial_id: int, include_relations: bool = False) -> Optional[Union[Financial, FinancialModel]]:
        """Obter um registro financeiro por ID"""
        query = self.db.query(FinancialModel).filter(FinancialModel.id == financial_id)
        query = self._configure_relations(query, include_relations)
        financial = query.first()
        
        if not financial:
            return None
        
        if include_relations:
            return financial  # Retorna o modelo com relacionamentos carregados
        return self._to_entity(financial)
    
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter todos os registros financeiros de um profile"""
        query = self.db.query(FinancialModel).filter(FinancialModel.profile_id == profile_id)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def get_by_banco(self, banco: str, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter todos os registros financeiros de um banco específico"""
        query = self.db.query(FinancialModel).filter(FinancialModel.banco == banco)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def get_by_tipo_conta(self, tipo_conta: TipoConta, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter registros financeiros por tipo de conta"""
        query = self.db.query(FinancialModel).filter(FinancialModel.tipo_conta == tipo_conta.value)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def get_by_tipo_chave_pix(self, tipo_chave_pix: TipoChavePix, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter registros financeiros por tipo de chave PIX"""
        query = self.db.query(FinancialModel).filter(FinancialModel.tipo_chave_pix == tipo_chave_pix.value)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def get_by_chave_pix(self, chave_pix: str, include_relations: bool = False) -> Optional[Union[Financial, FinancialModel]]:
        """Obter registro financeiro por chave PIX (deve ser único)"""
        query = self.db.query(FinancialModel).filter(FinancialModel.chave_pix == chave_pix)
        query = self._configure_relations(query, include_relations)
        financial = query.first()
        
        if not financial:
            return None
        
        if include_relations:
            return financial  # Retorna o modelo com relacionamentos carregados
        return self._to_entity(financial)
    
    def get_by_preferencia(self, preferencia: PreferenciaTransferencia, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter registros financeiros por preferência de transferência"""
        query = self.db.query(FinancialModel).filter(FinancialModel.preferencia == preferencia.value)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def get_by_cpf_cnpj(self, cpf_cnpj: str, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter registros financeiros por CPF/CNPJ"""
        query = self.db.query(FinancialModel).filter(FinancialModel.cpf_cnpj == cpf_cnpj)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def update(self, financial_id: int, financial: Financial) -> Optional[Financial]:
        """Atualizar um registro financeiro"""
        db_financial = self.db.query(FinancialModel).filter(FinancialModel.id == financial_id).first()
        
        if not db_financial:
            return None
        
        # Verificar se a chave PIX já existe (excluindo o registro atual)
        if financial.chave_pix != db_financial.chave_pix:
            if self.check_chave_pix_exists(financial.chave_pix, exclude_id=financial_id):
                raise ValueError(f"Chave PIX '{financial.chave_pix}' já está em uso")
        
        # Atualizar os campos (profile_id não pode ser alterado)
        if financial.banco:
            db_financial.banco = financial.banco
        if financial.agencia:
            db_financial.agencia = financial.agencia
        if financial.conta:
            db_financial.conta = financial.conta
        if financial.tipo_conta:
            db_financial.tipo_conta = financial.tipo_conta.value
        if financial.cpf_cnpj:
            db_financial.cpf_cnpj = financial.cpf_cnpj
        if financial.tipo_chave_pix:
            db_financial.tipo_chave_pix = financial.tipo_chave_pix.value
        if financial.chave_pix:
            db_financial.chave_pix = financial.chave_pix
        if financial.preferencia:
            db_financial.preferencia = financial.preferencia.value
        
        self.db.commit()
        self.db.refresh(db_financial)
        
        return self._to_entity(db_financial)
    
    def delete(self, financial_id: int) -> bool:
        """Deletar um registro financeiro"""
        financial = self.db.query(FinancialModel).filter(FinancialModel.id == financial_id).first()
        
        if not financial:
            return False
        
        self.db.delete(financial)
        self.db.commit()
        return True
    
    def get_all(self, include_relations: bool = False) -> List[Union[Financial, FinancialModel]]:
        """Obter todos os registros financeiros"""
        query = self.db.query(FinancialModel)
        query = self._configure_relations(query, include_relations)
        financials = query.all()
        
        if include_relations:
            return financials  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(financial) for financial in financials]
    
    def check_chave_pix_exists(self, chave_pix: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar se uma chave PIX já existe (para garantir unicidade)"""
        query = self.db.query(FinancialModel).filter(FinancialModel.chave_pix == chave_pix)
        
        if exclude_id:
            query = query.filter(FinancialModel.id != exclude_id)
        
        return query.first() is not None
    
    def _to_entity(self, model: FinancialModel) -> Financial:
        """Converter modelo para entidade"""
        return Financial(
            id=model.id,
            profile_id=model.profile_id,
            banco=model.banco,
            agencia=model.agencia,
            conta=model.conta,
            tipo_conta=TipoConta(model.tipo_conta),
            cpf_cnpj=model.cpf_cnpj,
            tipo_chave_pix=TipoChavePix(model.tipo_chave_pix),
            chave_pix=model.chave_pix,
            preferencia=PreferenciaTransferencia(model.preferencia),
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 