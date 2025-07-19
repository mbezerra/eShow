from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.role import Role, RoleType
from domain.repositories.role_repository import RoleRepository
from infrastructure.database.models.role_model import RoleModel

class RoleRepositoryImpl(RoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, role: Role) -> Role:
        """Criar um novo role"""
        db_role = RoleModel(role=role.role)
        self.session.add(db_role)
        self.session.commit()
        self.session.refresh(db_role)
        
        return Role(
            id=db_role.id,
            role=db_role.role,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at
        )

    def get_by_id(self, role_id: int) -> Optional[Role]:
        """Obter role por ID"""
        db_role = self.session.query(RoleModel).filter(RoleModel.id == role_id).first()
        if not db_role:
            return None
        
        return Role(
            id=db_role.id,
            role=db_role.role,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at
        )

    def get_by_role(self, role: RoleType) -> Optional[Role]:
        """Obter role por tipo"""
        db_role = self.session.query(RoleModel).filter(RoleModel.role == role).first()
        if not db_role:
            return None
        
        return Role(
            id=db_role.id,
            role=db_role.role,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Listar todos os roles com paginação"""
        db_roles = self.session.query(RoleModel).offset(skip).limit(limit).all()
        return [
            Role(
                id=db_role.id,
                role=db_role.role,
                created_at=db_role.created_at,
                updated_at=db_role.updated_at
            )
            for db_role in db_roles
        ]

    def update(self, role: Role) -> Role:
        """Atualizar role"""
        db_role = self.session.query(RoleModel).filter(RoleModel.id == role.id).first()
        if not db_role:
            raise ValueError("Role não encontrado")
        
        db_role.role = role.role
        db_role.updated_at = role.updated_at
        
        self.session.commit()
        self.session.refresh(db_role)
        
        return Role(
            id=db_role.id,
            role=db_role.role,
            created_at=db_role.created_at,
            updated_at=db_role.updated_at
        )

    def delete(self, role_id: int) -> bool:
        """Deletar role por ID"""
        db_role = self.session.query(RoleModel).filter(RoleModel.id == role_id).first()
        if not db_role:
            return False
        
        self.session.delete(db_role)
        self.session.commit()
        return True 