from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.musical_style import MusicalStyleCreate, MusicalStyleResponse, MusicalStyleUpdate
from app.application.services.musical_style_service import MusicalStyleService
from app.application.dependencies import get_musical_style_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/", response_model=MusicalStyleResponse, status_code=status.HTTP_201_CREATED)
def create_musical_style(
    style_data: MusicalStyleCreate,
    musical_style_service: MusicalStyleService = Depends(get_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        style = musical_style_service.create_musical_style(style_data)
        return style
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[MusicalStyleResponse])
def get_musical_styles(
    skip: int = 0,
    limit: int = 100,
    musical_style_service: MusicalStyleService = Depends(get_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    return musical_style_service.get_musical_styles(skip=skip, limit=limit)

@router.get("/{style_id}", response_model=MusicalStyleResponse)
def get_musical_style(
    style_id: int,
    musical_style_service: MusicalStyleService = Depends(get_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    style = musical_style_service.get_musical_style_by_id(style_id)
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estilo musical não encontrado"
        )
    return style

@router.put("/{style_id}", response_model=MusicalStyleResponse)
def update_musical_style(
    style_id: int,
    style_data: MusicalStyleUpdate,
    musical_style_service: MusicalStyleService = Depends(get_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        style = musical_style_service.update_musical_style(style_id, style_data)
        if not style:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estilo musical não encontrado"
            )
        return style
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{style_id}", status_code=status.HTTP_200_OK)
def delete_musical_style(
    style_id: int,
    musical_style_service: MusicalStyleService = Depends(get_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    success = musical_style_service.delete_musical_style(style_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estilo musical não encontrado"
        )
    return {"message": f"Estilo musical com ID {style_id} foi deletado com sucesso"} 