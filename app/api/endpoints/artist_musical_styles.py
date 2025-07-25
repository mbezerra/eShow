from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.schemas.artist_musical_style import (
    ArtistMusicalStyleCreate, 
    ArtistMusicalStyleResponse, 
    ArtistMusicalStyleListResponse,
    ArtistMusicalStyleBulkCreate
)
from app.application.services.artist_musical_style_service import ArtistMusicalStyleService
from app.application.dependencies import get_artist_musical_style_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_artist_musical_style_to_response(artist_musical_style):
    """Converter relacionamento para o schema de resposta"""
    data = {
        "artist_id": artist_musical_style.artist_id,
        "musical_style_id": artist_musical_style.musical_style_id,
        "created_at": artist_musical_style.created_at
    }
    
    # Adicionar id apenas se não for None
    if artist_musical_style.id is not None:
        data["id"] = artist_musical_style.id
    
    return ArtistMusicalStyleResponse.model_validate(data)

def convert_artist_musical_styles_list_to_response(artist_musical_styles):
    """Converter lista de relacionamentos para o schema de resposta"""
    converted_items = [convert_artist_musical_style_to_response(item) for item in artist_musical_styles]
    return ArtistMusicalStyleListResponse(items=converted_items)

router = APIRouter()

@router.post("/", response_model=ArtistMusicalStyleResponse, status_code=status.HTTP_201_CREATED)
def create_artist_musical_style(
    artist_musical_style_data: ArtistMusicalStyleCreate,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo relacionamento entre artista e estilo musical (requer autenticação)"""
    try:
        artist_musical_style = artist_musical_style_service.create_artist_musical_style(artist_musical_style_data)
        return convert_artist_musical_style_to_response(artist_musical_style)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/bulk", response_model=ArtistMusicalStyleListResponse, status_code=status.HTTP_201_CREATED)
def create_bulk_artist_musical_styles(
    bulk_data: ArtistMusicalStyleBulkCreate,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar múltiplos relacionamentos para um artista (requer autenticação)"""
    try:
        artist_musical_styles = artist_musical_style_service.create_bulk_artist_musical_styles(bulk_data)
        return convert_artist_musical_styles_list_to_response(artist_musical_styles)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/artist/{artist_id}")
def get_musical_styles_by_artist(
    artist_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os estilos musicais de um artista (requer autenticação)"""
    artist_musical_styles = artist_musical_style_service.get_musical_styles_by_artist(artist_id)
    return convert_artist_musical_styles_list_to_response(artist_musical_styles)

@router.get("/musical-style/{musical_style_id}")
def get_artists_by_musical_style(
    musical_style_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os artistas de um estilo musical (requer autenticação)"""
    artist_musical_styles = artist_musical_style_service.get_artists_by_musical_style(musical_style_id)
    return convert_artist_musical_styles_list_to_response(artist_musical_styles)

@router.put("/artist/{artist_id}")
def update_artist_musical_styles(
    artist_id: int,
    musical_style_ids: List[int],
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar todos os estilos musicais de um artista (substituir os existentes) (requer autenticação)"""
    try:
        artist_musical_styles = artist_musical_style_service.update_artist_musical_styles(artist_id, musical_style_ids)
        return convert_artist_musical_styles_list_to_response(artist_musical_styles)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/artist/{artist_id}", status_code=status.HTTP_200_OK)
def delete_all_artist_musical_styles(
    artist_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um artista (requer autenticação)"""
    success = artist_musical_style_service.delete_all_artist_musical_styles(artist_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este artista"
        )
    
    return {"message": f"Todos os relacionamentos do artista {artist_id} foram deletados com sucesso"}

@router.delete("/musical-style/{musical_style_id}", status_code=status.HTTP_200_OK)
def delete_all_musical_style_artists(
    musical_style_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um estilo musical (requer autenticação)"""
    success = artist_musical_style_service.delete_all_musical_style_artists(musical_style_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este estilo musical"
        )
    
    return {"message": f"Todos os relacionamentos do estilo musical {musical_style_id} foram deletados com sucesso"}

@router.get("/{artist_id}/{musical_style_id}")
def get_artist_musical_style(
    artist_id: int,
    musical_style_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um relacionamento específico (requer autenticação)"""
    artist_musical_style = artist_musical_style_service.get_artist_musical_style(artist_id, musical_style_id)
    if not artist_musical_style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )
    
    return convert_artist_musical_style_to_response(artist_musical_style)

@router.delete("/{artist_id}/{musical_style_id}", status_code=status.HTTP_200_OK)
def delete_artist_musical_style(
    artist_id: int,
    musical_style_id: int,
    artist_musical_style_service: ArtistMusicalStyleService = Depends(get_artist_musical_style_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um relacionamento específico (requer autenticação)"""
    success = artist_musical_style_service.delete_artist_musical_style(artist_id, musical_style_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )
    
    return {"message": f"Relacionamento entre artista {artist_id} e estilo musical {musical_style_id} foi deletado com sucesso"} 