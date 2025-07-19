from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.role import Role, RoleType

class RoleRepository(ABC):
    @abstractmethod
    def create(self, role: Role) -> Role:
        """Criar um novo role"""
        pass
    
    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[Role]:
        """Obter role por ID"""
        pass
    
    @abstractmethod
    def get_by_role(self, role: RoleType) -> Optional[Role]:
        """Obter role por tipo"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Listar todos os roles com paginação"""
        pass
    
    @abstractmethod
    def update(self, role: Role) -> Role:
        """Atualizar role"""
        pass
    
    @abstractmethod
    def delete(self, role_id: int) -> bool:
        """Deletar role por ID"""
        pass 