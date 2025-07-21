from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
import json
from app.schemas.artist import ArtistCreate, ArtistResponse, ArtistUpdate, ArtistResponseWithRelations, ArtistListResponse, ArtistListResponseWithRelations
from app.application.services.artist_service import ArtistService
from app.application.dependencies import get_artist_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_artist_to_response(artist, include_relations: bool = False):
    """Converter artista para o schema de resposta apropriado"""
    if include_relations:
        # Se include_relations=True, artist pode ser um ArtistModel
        from infrastructure.database.models.artist_model import ArtistModel
        if isinstance(artist, ArtistModel):
            # Converter o modelo do banco para o schema com relacionamentos
            return ArtistResponseWithRelations.model_validate({
                "id": artist.id,
                "profile_id": artist.profile_id,
                "artist_type_id": artist.artist_type_id,
                "dias_apresentacao": json.loads(artist.dias_apresentacao),
                "raio_atuacao": artist.raio_atuacao,
                "duracao_apresentacao": artist.duracao_apresentacao,
                "valor_hora": artist.valor_hora,
                "valor_couvert": artist.valor_couvert,
                "requisitos_minimos": artist.requisitos_minimos,
                "instagram": artist.instagram,
                "tiktok": artist.tiktok,
                "youtube": artist.youtube,
                "facebook": artist.facebook,
                "soundcloud": artist.soundcloud,
                "bandcamp": artist.bandcamp,
                "spotify": artist.spotify,
                "deezer": artist.deezer,
                "created_at": artist.created_at,
                "updated_at": artist.updated_at,
                "profile": artist.profile,
                "artist_type": artist.artist_type
            })
        else:
            return ArtistResponseWithRelations.model_validate(artist)
    else:
        return ArtistResponse.model_validate(artist)

def convert_artists_list_to_response(artists, include_relations: bool = False):
    """Converter lista de artistas para o schema de resposta apropriado"""
    converted_artists = [convert_artist_to_response(artist, include_relations) for artist in artists]
    if include_relations:
        return ArtistListResponseWithRelations(items=converted_artists)
    else:
        return ArtistListResponse(items=converted_artists)

router = APIRouter()

@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
def create_artist(
    artist_data: ArtistCreate,
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo artista (requer autenticação)"""
    try:
        artist = artist_service.create_artist(artist_data)
        return artist
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
def get_artists(
    skip: int = 0,
    limit: int = 100,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile e artist_type)"),
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Listar todos os artistas (requer autenticação)"""
    artists = artist_service.get_artists(skip=skip, limit=limit, include_relations=include_relations)
    
    return convert_artists_list_to_response(artists, include_relations)

@router.get("/{artist_id}")
def get_artist(
    artist_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile e artist_type)"),
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um artista específico (requer autenticação)"""
    artist = artist_service.get_artist_by_id(artist_id, include_relations=include_relations)
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artista não encontrado"
        )
    
    return convert_artist_to_response(artist, include_relations)

@router.get("/profile/{profile_id}")
def get_artist_by_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile e artist_type)"),
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter artista por ID do profile (requer autenticação)"""
    artist = artist_service.get_artist_by_profile_id(profile_id, include_relations=include_relations)
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artista não encontrado para este profile"
        )
    
    return convert_artist_to_response(artist, include_relations)

@router.get("/type/{artist_type_id}")
def get_artists_by_type(
    artist_type_id: int,
    skip: int = 0,
    limit: int = 100,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile e artist_type)"),
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Listar artistas por tipo (requer autenticação)"""
    artists = artist_service.get_artists_by_type(artist_type_id, skip=skip, limit=limit, include_relations=include_relations)
    
    return convert_artists_list_to_response(artists, include_relations)

@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    artist_data: ArtistUpdate,
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um artista (requer autenticação)"""
    try:
        artist = artist_service.update_artist(artist_id, artist_data)
        return artist
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{artist_id}", status_code=status.HTTP_200_OK)
def delete_artist(
    artist_id: int,
    artist_service: ArtistService = Depends(get_artist_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um artista (requer autenticação)"""
    success = artist_service.delete_artist(artist_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artista não encontrado"
        )
    
    return {"message": f"Artista com ID {artist_id} foi deletado com sucesso"} 