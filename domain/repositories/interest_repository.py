from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
from datetime import datetime, date
from domain.entities.interest import Interest, StatusInterest

class InterestRepository(ABC):
    """Interface do repositório para manifestações de interesse"""
    
    @abstractmethod
    def create(self, interest: Interest) -> Interest:
        """Criar uma nova manifestação de interesse"""
        pass
    
    @abstractmethod
    def get_by_id(self, interest_id: int, include_relations: bool = False) -> Optional[Union[Interest, Any]]:
        """Obter uma manifestação de interesse por ID"""
        pass
    
    @abstractmethod
    def get_by_profile_interessado(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse feitas por um profile"""
        pass
    
    @abstractmethod
    def get_by_profile_interesse(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse recebidas por um profile"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: StatusInterest, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse por status"""
        pass
    
    @abstractmethod
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse relacionadas a um space-event type"""
        pass
    
    @abstractmethod
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse relacionadas a um space-festival type"""
        pass
    
    @abstractmethod
    def get_by_date_range(self, data_inicio: date, data_fim: date, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse em um período"""
        pass
    
    @abstractmethod
    def get_by_profile_and_status(self, profile_id: int, status: StatusInterest, is_interessado: bool = True, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse de um profile filtradas por status
        
        Args:
            profile_id: ID do profile
            status: Status do interesse
            is_interessado: True para buscar como interessado, False para buscar como pessoa de interesse
            include_relations: Incluir dados relacionados
        """
        pass
    
    @abstractmethod
    def get_pending_for_profile(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse pendentes para um profile (recebidas e aguardando confirmação)"""
        pass
    
    @abstractmethod
    def get_statistics_by_profile(self, profile_id: int) -> dict:
        """Obter estatísticas de interesse para um profile"""
        pass
    
    @abstractmethod
    def update(self, interest_id: int, interest: Interest) -> Optional[Interest]:
        """Atualizar uma manifestação de interesse"""
        pass
    
    @abstractmethod
    def delete(self, interest_id: int) -> bool:
        """Deletar uma manifestação de interesse"""
        pass
    
    @abstractmethod
    def get_all(self, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse"""
        pass 