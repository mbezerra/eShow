from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.database.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        """Criar um novo usuário"""
        db_user = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            is_active=user.is_active
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obter usuário por ID"""
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def get_by_email(self, email: str) -> Optional[User]:
        """Obter usuário por email"""
        db_user = self.session.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Listar todos os usuários com paginação"""
        db_users = self.session.query(UserModel).offset(skip).limit(limit).all()
        return [
            User(
                id=db_user.id,
                name=db_user.name,
                email=db_user.email,
                password=db_user.password,
                is_active=db_user.is_active,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            for db_user in db_users
        ]

    def update(self, user: User) -> User:
        """Atualizar usuário"""
        db_user = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError("Usuário não encontrado")
        
        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        db_user.is_active = user.is_active
        db_user.updated_at = user.updated_at
        
        self.session.commit()
        self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def delete(self, user_id: int) -> bool:
        """Deletar usuário por ID"""
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return False
        
        self.session.delete(db_user)
        self.session.commit()
        return True 