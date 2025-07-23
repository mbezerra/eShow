from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.schemas.space_event_type import (
    SpaceEventTypeCreate, 
    SpaceEventTypeUpdate,
    SpaceEventTypeResponse, 
    SpaceEventTypeListResponse
)
from app.application.services.space_event_type_service import SpaceEventTypeService
from app.application.dependencies import get_space_event_type_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_space_event_type_to_response(space_event_type):
    """Converter relacionamento para o schema de resposta"""
    return SpaceEventTypeResponse.model_validate({
        "id": space_event_type.id,
        "space_id": space_event_type.space_id,
        "event_type_id": space_event_type.event_type_id,
        "tema": space_event_type.tema,
        "descricao": space_event_type.descricao,
        "link_divulgacao": space_event_type.link_divulgacao,
        "banner": space_event_type.banner,
        "data": space_event_type.data,
        "horario": space_event_type.horario,
        "created_at": space_event_type.created_at
    })

def convert_space_event_types_list_to_response(space_event_types):
    """Converter lista de relacionamentos para o schema de resposta"""
    converted_items = [convert_space_event_type_to_response(item) for item in space_event_types]
    return SpaceEventTypeListResponse(items=converted_items)

router = APIRouter()

@router.post("/", response_model=SpaceEventTypeResponse, status_code=status.HTTP_201_CREATED)
def create_space_event_type(
    space_event_type_data: SpaceEventTypeCreate,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo relacionamento entre espaço e tipo de evento (requer autenticação)"""
    try:
        space_event_type = space_event_type_service.create_space_event_type(space_event_type_data)
        return convert_space_event_type_to_response(space_event_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=SpaceEventTypeListResponse)
def get_all_space_event_types(
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os relacionamentos (requer autenticação)"""
    space_event_types = space_event_type_service.get_all_space_event_types()
    return convert_space_event_types_list_to_response(space_event_types)

@router.get("/space/{space_id}", response_model=SpaceEventTypeListResponse)
def get_event_types_by_space(
    space_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os tipos de eventos de um espaço (requer autenticação)"""
    space_event_types = space_event_type_service.get_event_types_by_space(space_id)
    return convert_space_event_types_list_to_response(space_event_types)

@router.get("/event-type/{event_type_id}", response_model=SpaceEventTypeListResponse)
def get_spaces_by_event_type(
    event_type_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os espaços de um tipo de evento (requer autenticação)"""
    space_event_types = space_event_type_service.get_spaces_by_event_type(event_type_id)
    return convert_space_event_types_list_to_response(space_event_types)

@router.get("/space/{space_id}/event-type/{event_type_id}", response_model=SpaceEventTypeListResponse)
def get_space_event_types_by_space_and_event_type(
    space_id: int,
    event_type_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter relacionamentos específicos entre espaço e tipo de evento (requer autenticação)"""
    space_event_types = space_event_type_service.get_space_event_types_by_space_and_event_type(space_id, event_type_id)
    return convert_space_event_types_list_to_response(space_event_types)

@router.get("/{space_event_type_id}", response_model=SpaceEventTypeResponse)
def get_space_event_type(
    space_event_type_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um relacionamento por ID (requer autenticação)"""
    space_event_type = space_event_type_service.get_space_event_type_by_id(space_event_type_id)
    if not space_event_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )
    
    return convert_space_event_type_to_response(space_event_type)

@router.put("/{space_event_type_id}", response_model=SpaceEventTypeResponse)
def update_space_event_type(
    space_event_type_id: int,
    space_event_type_data: SpaceEventTypeUpdate,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um relacionamento (requer autenticação)"""
    try:
        space_event_type = space_event_type_service.update_space_event_type(space_event_type_id, space_event_type_data)
        if not space_event_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relacionamento não encontrado"
            )
        return convert_space_event_type_to_response(space_event_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{space_event_type_id}", status_code=status.HTTP_200_OK)
def delete_space_event_type(
    space_event_type_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um relacionamento específico (requer autenticação)"""
    success = space_event_type_service.delete_space_event_type(space_event_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )
    
    return {"message": f"Relacionamento {space_event_type_id} foi deletado com sucesso"}

@router.delete("/space/{space_id}", status_code=status.HTTP_200_OK)
def delete_all_space_event_types_by_space(
    space_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um espaço (requer autenticação)"""
    success = space_event_type_service.delete_all_space_event_types_by_space(space_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este espaço"
        )
    
    return {"message": f"Todos os relacionamentos do espaço {space_id} foram deletados com sucesso"}

@router.delete("/event-type/{event_type_id}", status_code=status.HTTP_200_OK)
def delete_all_space_event_types_by_event_type(
    event_type_id: int,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um tipo de evento (requer autenticação)"""
    success = space_event_type_service.delete_all_space_event_types_by_event_type(event_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este tipo de evento"
        )
    
    return {"message": f"Todos os relacionamentos do tipo de evento {event_type_id} foram deletados com sucesso"} 