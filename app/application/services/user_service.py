from typing import List, Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from infrastructure.database.models.user_model import UserModel

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Criar um novo usuário"""
        # Verificar se o email já existe
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email já está em uso")

        # Criar entidade de domínio
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,  # Senha já vem hasheada do AuthService
            is_active=user_data.is_active
        )

        # Salvar no repositório
        created_user = self.user_repository.create(user)
        
        # Converter para schema de resposta
        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Listar usuários com paginação"""
        users = self.user_repository.get_all(skip=skip, limit=limit)
        return [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Obter usuário por ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Obter usuário por email"""
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,  # Incluir senha para autenticação
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Atualizar usuário"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None

        # Atualizar campos fornecidos
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.email is not None:
            # Verificar se o novo email já existe
            existing_user = self.user_repository.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email já está em uso")
            user.email = user_data.email
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        # Salvar alterações
        updated_user = self.user_repository.update(user)
        
        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )

    def delete_user(self, user_id: int) -> bool:
        """Deletar usuário"""
        return self.user_repository.delete(user_id) 