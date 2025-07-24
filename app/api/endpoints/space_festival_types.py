from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.schemas.space_festival_type import (
    SpaceFestivalTypeCreate, 
    SpaceFestivalTypeUpdate,
    SpaceFestivalTypeStatusUpdate,
    SpaceFestivalTypeResponse, 
    SpaceFestivalTypeListResponse
)
from app.application.services.space_festival_type_service import SpaceFestivalTypeService
from app.application.dependencies import get_space_festival_type_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_space_festival_type_to_response(space_festival_type):
    """Converter relacionamento para o schema de resposta"""
    return SpaceFestivalTypeResponse.model_validate({
        "id": space_festival_type.id,
        "space_id": space_festival_type.space_id,
        "festival_type_id": space_festival_type.festival_type_id,
        "tema": space_festival_type.tema,
        "descricao": space_festival_type.descricao,
        "status": space_festival_type.status,
        "link_divulgacao": space_festival_type.link_divulgacao,
        "banner": space_festival_type.banner,
        "data": space_festival_type.data,
        "horario": space_festival_type.horario,
        "created_at": space_festival_type.created_at
    })

def convert_space_festival_types_list_to_response(space_festival_types):
    """Converter lista de relacionamentos para o schema de resposta"""
    converted_items = [convert_space_festival_type_to_response(item) for item in space_festival_types]
    return SpaceFestivalTypeListResponse(items=converted_items)

router = APIRouter()

@router.post("/", response_model=SpaceFestivalTypeResponse, status_code=status.HTTP_201_CREATED)
def create_space_festival_type(
    space_festival_type_data: SpaceFestivalTypeCreate,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo relacionamento entre espaço e tipo de festival (requer autenticação)"""
    try:
        space_festival_type = space_festival_type_service.create_space_festival_type(space_festival_type_data)
        return convert_space_festival_type_to_response(space_festival_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=SpaceFestivalTypeListResponse)
def get_all_space_festival_types(
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os relacionamentos (requer autenticação)"""
    space_festival_types = space_festival_type_service.get_all_space_festival_types()
    return convert_space_festival_types_list_to_response(space_festival_types)

@router.get("/space/{space_id}", response_model=SpaceFestivalTypeListResponse)
def get_festival_types_by_space(
    space_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os tipos de festivais de um espaço (requer autenticação)"""
    space_festival_types = space_festival_type_service.get_festival_types_by_space(space_id)
    return convert_space_festival_types_list_to_response(space_festival_types)

@router.get("/festival-type/{festival_type_id}", response_model=SpaceFestivalTypeListResponse)
def get_spaces_by_festival_type(
    festival_type_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os espaços de um tipo de festival (requer autenticação)"""
    space_festival_types = space_festival_type_service.get_spaces_by_festival_type(festival_type_id)
    return convert_space_festival_types_list_to_response(space_festival_types)

@router.get("/space/{space_id}/festival-type/{festival_type_id}", response_model=SpaceFestivalTypeListResponse)
def get_space_festival_types_by_space_and_festival_type(
    space_id: int,
    festival_type_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter relacionamentos específicos entre espaço e tipo de festival (requer autenticação)"""
    space_festival_types = space_festival_type_service.get_space_festival_types_by_space_and_festival_type(space_id, festival_type_id)
    return convert_space_festival_types_list_to_response(space_festival_types)

@router.get("/{space_festival_type_id}", response_model=SpaceFestivalTypeResponse)
def get_space_festival_type(
    space_festival_type_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um relacionamento por ID (requer autenticação)"""
    space_festival_type = space_festival_type_service.get_space_festival_type_by_id(space_festival_type_id)
    if not space_festival_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )

    return convert_space_festival_type_to_response(space_festival_type)

@router.put("/{space_festival_type_id}", response_model=SpaceFestivalTypeResponse)
def update_space_festival_type(
    space_festival_type_id: int,
    space_festival_type_data: SpaceFestivalTypeUpdate,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um relacionamento (requer autenticação)"""
    try:
        space_festival_type = space_festival_type_service.update_space_festival_type(space_festival_type_id, space_festival_type_data)
        if not space_festival_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relacionamento não encontrado"
            )
        return convert_space_festival_type_to_response(space_festival_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{space_festival_type_id}/status", response_model=SpaceFestivalTypeResponse)
def update_space_festival_type_status(
    space_festival_type_id: int,
    status_data: SpaceFestivalTypeStatusUpdate,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar apenas o status de um relacionamento (requer autenticação)"""
    try:
        space_festival_type = space_festival_type_service.update_space_festival_type_status(space_festival_type_id, status_data.status)
        if not space_festival_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relacionamento não encontrado"
            )
        return convert_space_festival_type_to_response(space_festival_type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{space_festival_type_id}", status_code=status.HTTP_200_OK)
def delete_space_festival_type(
    space_festival_type_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um relacionamento específico (requer autenticação)"""
    success = space_festival_type_service.delete_space_festival_type(space_festival_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacionamento não encontrado"
        )

    return {"message": f"Relacionamento {space_festival_type_id} foi deletado com sucesso"}

@router.delete("/space/{space_id}", status_code=status.HTTP_200_OK)
def delete_all_space_festival_types_by_space(
    space_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um espaço (requer autenticação)"""
    success = space_festival_type_service.delete_all_space_festival_types_by_space(space_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este espaço"
        )

    return {"message": f"Todos os relacionamentos do espaço {space_id} foram deletados com sucesso"}

@router.delete("/festival-type/{festival_type_id}", status_code=status.HTTP_200_OK)
def delete_all_space_festival_types_by_festival_type(
    festival_type_id: int,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar todos os relacionamentos de um tipo de festival (requer autenticação)"""
    success = space_festival_type_service.delete_all_space_festival_types_by_festival_type(festival_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum relacionamento encontrado para este tipo de festival"
        )

    return {"message": f"Todos os relacionamentos do tipo de festival {festival_type_id} foram deletados com sucesso"} 