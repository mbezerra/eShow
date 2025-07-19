from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.profile import Profile

class ProfileRepository(ABC):
    @abstractmethod
    def create(self, profile: Profile) -> Profile:
        """Criar um novo profile"""
        pass
    
    @abstractmethod
    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Obter profile por ID"""
        pass
    
    @abstractmethod
    def get_by_role_id(self, role_id: int) -> List[Profile]:
        """Obter profiles por role_id"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Listar todos os profiles com paginação"""
        pass
    
    @abstractmethod
    def update(self, profile: Profile) -> Profile:
        """Atualizar profile"""
        pass
    
    @abstractmethod
    def delete(self, profile_id: int) -> bool:
        """Deletar profile por ID"""
        pass 