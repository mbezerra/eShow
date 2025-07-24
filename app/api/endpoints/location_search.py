from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from infrastructure.database.database import get_database_session
from app.application.services.location_search_service import LocationSearchService
from app.schemas.location_search import (
    LocationSearchResponse,
    LocationSearchRequest
)
from app.schemas.user import UserResponse
from infrastructure.repositories.artist_repository_impl import ArtistRepositoryImpl
from infrastructure.repositories.space_repository_impl import SpaceRepositoryImpl
from infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from infrastructure.repositories.space_event_type_repository_impl import SpaceEventTypeRepositoryImpl
from infrastructure.repositories.space_festival_type_repository_impl import SpaceFestivalTypeRepositoryImpl
from infrastructure.repositories.booking_repository_impl import BookingRepositoryImpl

router = APIRouter()

def get_location_search_service(db: Session = Depends(get_database_session)) -> LocationSearchService:
    """Dependency para obter o serviço de busca por localização"""
    artist_repository = ArtistRepositoryImpl(db)
    space_repository = SpaceRepositoryImpl(db)
    profile_repository = ProfileRepositoryImpl(db)
    space_event_type_repository = SpaceEventTypeRepositoryImpl(db)
    space_festival_type_repository = SpaceFestivalTypeRepositoryImpl(db)
    booking_repository = BookingRepositoryImpl(db)
    
    return LocationSearchService(
        artist_repository=artist_repository,
        space_repository=space_repository,
        profile_repository=profile_repository,
        space_event_type_repository=space_event_type_repository,
        space_festival_type_repository=space_festival_type_repository,
        booking_repository=booking_repository
    )

@router.get("/spaces-for-artist", response_model=LocationSearchResponse)
async def search_spaces_for_artist(
    return_full_data: bool = Query(True, description="Retornar dados completos ou apenas IDs"),
    max_results: Optional[int] = Query(100, description="Limite máximo de resultados"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session),
    location_service: LocationSearchService = Depends(get_location_search_service)
):
    """
    Endpoint 1: Buscar espaços para um artista baseado no seu raio de atuação
    
    - Verifica o raio de atuação do artista logado
    - Busca espaços (role_id = 3) dentro do raio
    - Filtra apenas espaços com eventos/festivais com status CONTRATANDO
    """
    try:
        # Obter o profile do artista logado
        profile_repository = ProfileRepositoryImpl(db)
        artist_profile = profile_repository.get_by_user_id(current_user.id)
        
        if not artist_profile:
            raise HTTPException(status_code=404, detail="Profile do artista não encontrado")
        
        # Verificar se o usuário é realmente um artista (role_id = 2)
        if artist_profile.role_id != 2:
            raise HTTPException(status_code=403, detail="Apenas artistas podem usar este endpoint")
        
        # Realizar a busca
        result = location_service.search_spaces_for_artist(
            db=db,
            artist_profile_id=artist_profile.id,
            return_full_data=return_full_data,
            max_results=max_results
        )
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.get("/artists-for-space", response_model=LocationSearchResponse)
async def search_artists_for_space(
    return_full_data: bool = Query(True, description="Retornar dados completos ou apenas IDs"),
    max_results: Optional[int] = Query(100, description="Limite máximo de resultados"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session),
    location_service: LocationSearchService = Depends(get_location_search_service)
):
    """
    Endpoint 2: Buscar artistas para um espaço baseado no raio de atuação dos artistas
    
    - Verifica o CEP do espaço logado
    - Busca artistas (role_id = 2) dentro do raio de atuação de cada artista
    - Filtra apenas artistas disponíveis (sem agendamentos conflitantes)
    """
    try:
        # Obter o profile do espaço logado
        profile_repository = ProfileRepositoryImpl(db)
        space_profile = profile_repository.get_by_user_id(current_user.id)
        
        if not space_profile:
            raise HTTPException(status_code=404, detail="Profile do espaço não encontrado")
        
        # Verificar se o usuário é realmente um espaço (role_id = 3)
        if space_profile.role_id != 3:
            raise HTTPException(status_code=403, detail="Apenas espaços podem usar este endpoint")
        
        # Realizar a busca
        result = location_service.search_artists_for_space(
            db=db,
            space_profile_id=space_profile.id,
            return_full_data=return_full_data,
            max_results=max_results
        )
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.post("/spaces-for-artist", response_model=LocationSearchResponse)
async def search_spaces_for_artist_post(
    request: LocationSearchRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session),
    location_service: LocationSearchService = Depends(get_location_search_service)
):
    """
    Versão POST do endpoint de busca de espaços para artista
    """
    try:
        # Obter o profile do artista logado
        profile_repository = ProfileRepositoryImpl(db)
        artist_profile = profile_repository.get_by_user_id(current_user.id)
        
        if not artist_profile:
            raise HTTPException(status_code=404, detail="Profile do artista não encontrado")
        
        # Verificar se o usuário é realmente um artista (role_id = 2)
        if artist_profile.role_id != 2:
            raise HTTPException(status_code=403, detail="Apenas artistas podem usar este endpoint")
        
        # Realizar a busca
        result = location_service.search_spaces_for_artist(
            db=db,
            artist_profile_id=artist_profile.id,
            return_full_data=request.return_full_data,
            max_results=request.max_results
        )
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@router.post("/artists-for-space", response_model=LocationSearchResponse)
async def search_artists_for_space_post(
    request: LocationSearchRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_database_session),
    location_service: LocationSearchService = Depends(get_location_search_service)
):
    """
    Versão POST do endpoint de busca de artistas para espaço
    """
    try:
        # Obter o profile do espaço logado
        profile_repository = ProfileRepositoryImpl(db)
        space_profile = profile_repository.get_by_user_id(current_user.id)
        
        if not space_profile:
            raise HTTPException(status_code=404, detail="Profile do espaço não encontrado")
        
        # Verificar se o usuário é realmente um espaço (role_id = 3)
        if space_profile.role_id != 3:
            raise HTTPException(status_code=403, detail="Apenas espaços podem usar este endpoint")
        
        # Realizar a busca
        result = location_service.search_artists_for_space(
            db=db,
            space_profile_id=space_profile.id,
            return_full_data=request.return_full_data,
            max_results=request.max_results
        )
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}") 