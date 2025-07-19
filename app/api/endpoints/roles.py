from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.application.services.role_service import RoleService
from app.application.dependencies import get_role_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo role (requer autenticação)"""
    try:
        role = role_service.create_role(role_data)
        return role
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[RoleResponse])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Listar todos os roles (requer autenticação)"""
    roles = role_service.get_roles(skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um role específico (requer autenticação)"""
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role não encontrado"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um role (requer autenticação)"""
    try:
        role = role_service.update_role(role_id, role_data)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role não encontrado"
            )
        return role
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(
    role_id: int,
    role_service: RoleService = Depends(get_role_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um role (requer autenticação)"""
    success = role_service.delete_role(role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role não encontrado"
        )
    
    return {"message": f"Role com ID {role_id} foi deletado com sucesso"} 