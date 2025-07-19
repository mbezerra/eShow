from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User

class UserRepository(ABC):
    """Interface do repositório de usuários"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Criar um novo usuário"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obter usuário por ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar todos os usuários com paginação"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Atualizar usuário"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Deletar usuário por ID"""
        pass 