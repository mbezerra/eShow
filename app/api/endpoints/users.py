from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.application.services.user_service import UserService
from app.application.dependencies import get_user_service
from app.core.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Criar um novo usuário"""
    try:
        user = user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter informações do usuário atual"""
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Listar todos os usuários (requer autenticação)"""
    users = user_service.get_users(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um usuário específico (requer autenticação)"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um usuário (requer autenticação)"""
    try:
        user = user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um usuário (requer autenticação)"""
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {"message": f"Usuário com ID {user_id} foi deletado com sucesso"} 