from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from app.application.services.profile_service import ProfileService
from app.application.dependencies import get_profile_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: ProfileCreate,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo profile (requer autenticação)"""
    try:
        profile = profile_service.create_profile(profile_data)
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ProfileResponse])
def get_profiles(
    skip: int = 0,
    limit: int = 100,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Listar todos os profiles (requer autenticação)"""
    profiles = profile_service.get_profiles(skip=skip, limit=limit)
    return profiles

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um profile específico (requer autenticação)"""
    profile = profile_service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile não encontrado"
        )
    return profile

@router.get("/role/{role_id}", response_model=List[ProfileResponse])
def get_profiles_by_role(
    role_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter profiles por role_id (requer autenticação)"""
    profiles = profile_service.get_profiles_by_role_id(role_id)
    return profiles

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um profile (requer autenticação)"""
    try:
        profile = profile_service.update_profile(profile_id, profile_data)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile não encontrado"
            )
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{profile_id}", status_code=status.HTTP_200_OK)
def delete_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um profile (requer autenticação)"""
    success = profile_service.delete_profile(profile_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile não encontrado"
        )
    
    return {"message": f"Profile com ID {profile_id} foi deletado com sucesso"} 