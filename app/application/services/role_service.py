from typing import List, Optional
from domain.entities.role import Role, RoleType
from domain.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role(self, role_data: RoleCreate) -> RoleResponse:
        """Criar um novo role"""
        # Verificar se o role já existe
        existing_role = self.role_repository.get_by_role(role_data.role)
        if existing_role:
            raise ValueError("Role já existe")

        # Criar entidade de domínio
        role = Role(role=role_data.role)

        # Salvar no repositório
        created_role = self.role_repository.create(role)
        
        # Converter para schema de resposta
        return RoleResponse(
            id=created_role.id,
            role=created_role.role,
            created_at=created_role.created_at,
            updated_at=created_role.updated_at
        )

    def get_roles(self, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
        """Listar roles com paginação"""
        roles = self.role_repository.get_all(skip=skip, limit=limit)
        return [
            RoleResponse(
                id=role.id,
                role=role.role,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            for role in roles
        ]

    def get_role_by_id(self, role_id: int) -> Optional[RoleResponse]:
        """Obter role por ID"""
        role = self.role_repository.get_by_id(role_id)
        if not role:
            return None
        
        return RoleResponse(
            id=role.id,
            role=role.role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )

    def get_role_by_type(self, role_type: RoleType) -> Optional[RoleResponse]:
        """Obter role por tipo"""
        role = self.role_repository.get_by_role(role_type)
        if not role:
            return None
        
        return RoleResponse(
            id=role.id,
            role=role.role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )

    def update_role(self, role_id: int, role_data: RoleUpdate) -> Optional[RoleResponse]:
        """Atualizar role"""
        role = self.role_repository.get_by_id(role_id)
        if not role:
            return None

        # Atualizar campos fornecidos
        if role_data.role is not None:
            # Verificar se o novo role já existe
            existing_role = self.role_repository.get_by_role(role_data.role)
            if existing_role and existing_role.id != role_id:
                raise ValueError("Role já existe")
            role.role = role_data.role

        # Salvar alterações
        updated_role = self.role_repository.update(role)
        
        return RoleResponse(
            id=updated_role.id,
            role=updated_role.role,
            created_at=updated_role.created_at,
            updated_at=updated_role.updated_at
        )

    def delete_role(self, role_id: int) -> bool:
        """Deletar role"""
        return self.role_repository.delete(role_id) 