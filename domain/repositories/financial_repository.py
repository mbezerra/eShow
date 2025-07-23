from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
from domain.entities.financial import Financial, TipoConta, TipoChavePix, PreferenciaTransferencia

class FinancialRepository(ABC):
    """Interface do repositório para dados financeiros/bancários"""
    
    @abstractmethod
    def create(self, financial: Financial) -> Financial:
        """Criar um novo registro financeiro"""
        pass
    
    @abstractmethod
    def get_by_id(self, financial_id: int, include_relations: bool = False) -> Optional[Union[Financial, Any]]:
        """Obter um registro financeiro por ID"""
        pass
    
    @abstractmethod
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros de um profile"""
        pass
    
    @abstractmethod
    def get_by_banco(self, banco: int, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros de um banco específico"""
        pass
    
    @abstractmethod
    def get_by_tipo_conta(self, tipo_conta: TipoConta, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por tipo de conta"""
        pass
    
    @abstractmethod
    def get_by_tipo_chave_pix(self, tipo_chave_pix: TipoChavePix, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por tipo de chave PIX"""
        pass
    
    @abstractmethod
    def get_by_chave_pix(self, chave_pix: str, include_relations: bool = False) -> Optional[Union[Financial, Any]]:
        """Obter registro financeiro por chave PIX (deve ser único)"""
        pass
    
    @abstractmethod
    def get_by_preferencia(self, preferencia: PreferenciaTransferencia, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por preferência de transferência"""
        pass
    
    @abstractmethod
    def get_by_cpf_cnpj(self, cpf_cnpj: str, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter registros financeiros por CPF/CNPJ"""
        pass
    
    @abstractmethod
    def update(self, financial_id: int, financial: Financial) -> Optional[Financial]:
        """Atualizar um registro financeiro"""
        pass
    
    @abstractmethod
    def delete(self, financial_id: int) -> bool:
        """Deletar um registro financeiro"""
        pass
    
    @abstractmethod
    def get_all(self, include_relations: bool = False) -> List[Union[Financial, Any]]:
        """Obter todos os registros financeiros"""
        pass
    
    @abstractmethod
    def check_chave_pix_exists(self, chave_pix: str, exclude_id: Optional[int] = None) -> bool:
        """Verificar se uma chave PIX já existe (para garantir unicidade)"""
        pass 