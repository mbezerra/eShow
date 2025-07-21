from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.artist_type import ArtistTypeCreate, ArtistTypeResponse, ArtistTypeUpdate
from app.application.services.artist_type_service import ArtistTypeService
from app.application.dependencies import get_artist_type_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/", response_model=ArtistTypeResponse, status_code=status.HTTP_201_CREATED)
def create_artist_type(
    artist_type_data: ArtistTypeCreate,
    artist_type_service: ArtistTypeService = Depends(get_artist_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        artist_type = artist_type_service.create_artist_type(artist_type_data)
        return artist_type
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ArtistTypeResponse])
def get_artist_types(
    skip: int = 0,
    limit: int = 100,
    artist_type_service: ArtistTypeService = Depends(get_artist_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    return artist_type_service.get_artist_types(skip=skip, limit=limit)

@router.get("/{artist_type_id}", response_model=ArtistTypeResponse)
def get_artist_type(
    artist_type_id: int,
    artist_type_service: ArtistTypeService = Depends(get_artist_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    artist_type = artist_type_service.get_artist_type_by_id(artist_type_id)
    if not artist_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de artista não encontrado"
        )
    return artist_type

@router.put("/{artist_type_id}", response_model=ArtistTypeResponse)
def update_artist_type(
    artist_type_id: int,
    artist_type_data: ArtistTypeUpdate,
    artist_type_service: ArtistTypeService = Depends(get_artist_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        artist_type = artist_type_service.update_artist_type(artist_type_id, artist_type_data)
        if not artist_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de artista não encontrado"
            )
        return artist_type
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{artist_type_id}", status_code=status.HTTP_200_OK)
def delete_artist_type(
    artist_type_id: int,
    artist_type_service: ArtistTypeService = Depends(get_artist_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    success = artist_type_service.delete_artist_type(artist_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de artista não encontrado"
        )
    return {"message": f"Tipo de artista com ID {artist_type_id} foi deletado com sucesso"} 