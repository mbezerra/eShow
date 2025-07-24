from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Union
from datetime import date
from app.schemas.interest import (
    InterestCreate,
    InterestUpdate,
    InterestResponse,
    InterestListResponse,
    InterestWithRelations,
    InterestListWithRelations,
    InterestStatusUpdate,
    InterestStatistics,
    StatusInterestEnum
)
from app.application.services.interest_service import InterestService
from app.application.dependencies import get_interest_service, get_profile_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse
from domain.entities.interest import StatusInterest

def convert_interest_to_response(interest, include_relations: bool = False):
    """Converter manifestação de interesse para o schema de resposta apropriado"""
    if include_relations:
        # Se include_relations=True, interest pode ser um InterestModel
        from infrastructure.database.models.interest_model import InterestModel
        if isinstance(interest, InterestModel):
            # Converter o modelo do banco para o schema com relacionamentos
            return InterestWithRelations.model_validate({
                "id": interest.id,
                "profile_id_interessado": interest.profile_id_interessado,
                "profile_id_interesse": interest.profile_id_interesse,
                "data_inicial": interest.data_inicial,
                "horario_inicial": interest.horario_inicial,
                "duracao_apresentacao": interest.duracao_apresentacao,
                "valor_hora_ofertado": interest.valor_hora_ofertado,
                "valor_couvert_ofertado": interest.valor_couvert_ofertado,
                "space_event_type_id": interest.space_event_type_id,
                "space_festival_type_id": interest.space_festival_type_id,
                "mensagem": interest.mensagem,
                "resposta": interest.resposta,
                "status": interest.status,
                "created_at": interest.created_at,
                "updated_at": interest.updated_at,
                "profile_interessado": interest.profile_interessado,
                "profile_interesse": interest.profile_interesse,
                "space_event_type": interest.space_event_type,
                "space_festival_type": interest.space_festival_type
            })
        else:
            return InterestWithRelations.model_validate(interest)
    else:
        return InterestResponse.model_validate({
            "id": interest.id,
            "profile_id_interessado": interest.profile_id_interessado,
            "profile_id_interesse": interest.profile_id_interesse,
            "data_inicial": interest.data_inicial,
            "horario_inicial": interest.horario_inicial,
            "duracao_apresentacao": interest.duracao_apresentacao,
            "valor_hora_ofertado": interest.valor_hora_ofertado,
            "valor_couvert_ofertado": interest.valor_couvert_ofertado,
            "space_event_type_id": interest.space_event_type_id,
            "space_festival_type_id": interest.space_festival_type_id,
            "mensagem": interest.mensagem,
            "resposta": interest.resposta,
            "status": interest.status,
            "created_at": interest.created_at,
            "updated_at": interest.updated_at
        })

def convert_interests_list_to_response(interests, include_relations: bool = False):
    """Converter lista de manifestações de interesse para o schema de resposta apropriado"""
    converted_interests = [convert_interest_to_response(interest, include_relations) for interest in interests]
    if include_relations:
        return InterestListWithRelations(items=converted_interests)
    else:
        return InterestListResponse(items=converted_interests)

router = APIRouter()

@router.post("/", response_model=InterestResponse, status_code=status.HTTP_201_CREATED)
def create_interest(
    interest_data: InterestCreate,
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar uma nova manifestação de interesse (requer autenticação)"""
    try:
        interest = interest_service.create_interest(interest_data)
        return convert_interest_to_response(interest)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
def get_all_interests(
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todas as manifestações de interesse (requer autenticação)"""
    interests = interest_service.get_all_interests(include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/{interest_id}")
def get_interest_by_id(
    interest_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter uma manifestação de interesse por ID (requer autenticação)"""
    interest = interest_service.get_interest_by_id(interest_id, include_relations=include_relations)
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manifestação de interesse não encontrada"
        )
    return convert_interest_to_response(interest, include_relations=include_relations)

@router.get("/profile/interessado/{profile_id}")
def get_interests_by_profile_interessado(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todas as manifestações de interesse feitas por um profile (requer autenticação)"""
    interests = interest_service.get_interests_by_profile_interessado(profile_id, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/profile/interesse/{profile_id}")
def get_interests_by_profile_interesse(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todas as manifestações de interesse recebidas por um profile (requer autenticação)"""
    interests = interest_service.get_interests_by_profile_interesse(profile_id, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/profile/{profile_id}/pending")
def get_pending_interests_for_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse pendentes para um profile (requer autenticação)"""
    interests = interest_service.get_pending_interests_for_profile(profile_id, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/profile/{profile_id}/statistics", response_model=InterestStatistics)
def get_interest_statistics(
    profile_id: int,
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter estatísticas de interesse para um profile (requer autenticação)"""
    stats = interest_service.get_interest_statistics(profile_id)
    return InterestStatistics.model_validate(stats)

@router.get("/status/{status}")
def get_interests_by_status(
    status: StatusInterestEnum,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse por status (requer autenticação)"""
    # Converter enum do schema para enum da entidade
    status_entity = StatusInterest(status.value)
    interests = interest_service.get_interests_by_status(status_entity, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/profile/{profile_id}/status/{status}")
def get_interests_by_profile_and_status(
    profile_id: int,
    status: StatusInterestEnum,
    is_interessado: bool = Query(True, description="True para buscar como interessado, False para buscar como pessoa de interesse"),
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse de um profile filtradas por status (requer autenticação)"""
    # Converter enum do schema para enum da entidade
    status_entity = StatusInterest(status.value)
    interests = interest_service.get_interests_by_profile_and_status(
        profile_id, status_entity, is_interessado, include_relations=include_relations
    )
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/space-event-type/{space_event_type_id}")
def get_interests_by_space_event_type(
    space_event_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse relacionadas a um space-event type (requer autenticação)"""
    interests = interest_service.get_interests_by_space_event_type(space_event_type_id, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/space-festival-type/{space_festival_type_id}")
def get_interests_by_space_festival_type(
    space_festival_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse relacionadas a um space-festival type (requer autenticação)"""
    interests = interest_service.get_interests_by_space_festival_type(space_festival_type_id, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.get("/date-range/")
def get_interests_by_date_range(
    data_inicio: date = Query(..., description="Data inicial (formato: YYYY-MM-DD)"),
    data_fim: date = Query(..., description="Data final (formato: YYYY-MM-DD)"),
    include_relations: bool = Query(False, description="Incluir dados relacionados (profiles, space_event_type, space_festival_type)"),
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter manifestações de interesse em um período (requer autenticação)"""
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data final deve ser posterior à data inicial"
        )
    
    interests = interest_service.get_interests_by_date_range(data_inicio, data_fim, include_relations=include_relations)
    return convert_interests_list_to_response(interests, include_relations=include_relations)

@router.put("/{interest_id}", response_model=InterestResponse)
def update_interest(
    interest_id: int,
    interest_data: InterestUpdate,
    interest_service: InterestService = Depends(get_interest_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar uma manifestação de interesse (requer autenticação)"""
    try:
        updated_interest = interest_service.update_interest(interest_id, interest_data)
        if not updated_interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manifestação de interesse não encontrada"
            )
        return convert_interest_to_response(updated_interest)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{interest_id}/status", response_model=InterestResponse)
def update_interest_status(
    interest_id: int,
    status_data: InterestStatusUpdate,
    interest_service: InterestService = Depends(get_interest_service),
    profile_service = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar status de uma manifestação de interesse (aceitar/recusar) (requer autenticação)"""
    try:
        # Obter profile do usuário atual
        profile = profile_service.get_profile_by_user_id(current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile do usuário não encontrado"
            )
        
        # Converter enum do schema para enum da entidade
        status_entity = StatusInterest(status_data.status.value)
        updated_status_data = InterestStatusUpdate(
            status=status_entity,
            resposta=status_data.resposta
        )
        
        updated_interest = interest_service.update_interest_status(
            interest_id, updated_status_data, profile.id
        )
        if not updated_interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manifestação de interesse não encontrada"
            )
        return convert_interest_to_response(updated_interest)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{interest_id}/accept", response_model=InterestResponse)
def accept_interest(
    interest_id: int,
    resposta: Optional[str] = Query(None, description="Resposta opcional ao aceitar"),
    interest_service: InterestService = Depends(get_interest_service),
    profile_service = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Aceitar uma manifestação de interesse (requer autenticação)"""
    try:
        # Obter profile do usuário atual
        profile = profile_service.get_profile_by_user_id(current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile do usuário não encontrado"
            )
        
        updated_interest = interest_service.accept_interest(interest_id, profile.id, resposta)
        if not updated_interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manifestação de interesse não encontrada"
            )
        return convert_interest_to_response(updated_interest)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{interest_id}/reject", response_model=InterestResponse)
def reject_interest(
    interest_id: int,
    resposta: Optional[str] = Query(None, description="Resposta opcional ao recusar"),
    interest_service: InterestService = Depends(get_interest_service),
    profile_service = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Recusar uma manifestação de interesse (requer autenticação)"""
    try:
        # Obter profile do usuário atual
        profile = profile_service.get_profile_by_user_id(current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile do usuário não encontrado"
            )
        
        updated_interest = interest_service.reject_interest(interest_id, profile.id, resposta)
        if not updated_interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manifestação de interesse não encontrada"
            )
        return convert_interest_to_response(updated_interest)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{interest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interest(
    interest_id: int,
    interest_service: InterestService = Depends(get_interest_service),
    profile_service = Depends(get_profile_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar uma manifestação de interesse (requer autenticação)"""
    try:
        # Obter profile do usuário atual
        profile = profile_service.get_profile_by_user_id(current_user.id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile do usuário não encontrado"
            )
        
        success = interest_service.delete_interest(interest_id, profile.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manifestação de interesse não encontrada"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 