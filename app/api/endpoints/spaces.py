from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.space import SpaceCreate, SpaceUpdate, SpaceResponse, SpaceResponseWithRelations
from app.application.services.space_service import SpaceService
from app.application.dependencies import get_space_service

router = APIRouter()

@router.post("/", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
def create_space(
    space: SpaceCreate,
    space_service: SpaceService = Depends(get_space_service)
):
    """Criar um novo espaço"""
    try:
        space_data = space.dict()
        return space_service.create_space(space_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
def get_spaces(
    skip: int = 0,
    limit: int = 100,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Listar todos os espaços"""
    return space_service.get_all_spaces(skip=skip, limit=limit, include_relations=include_relations)

@router.get("/{space_id}")
def get_space(
    space_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Buscar um espaço por ID"""
    space = space_service.get_space_by_id(space_id, include_relations=include_relations)
    if not space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space não encontrado"
        )
    return space

@router.get("/profile/{profile_id}")
def get_spaces_by_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Buscar espaços por profile ID"""
    return space_service.get_spaces_by_profile_id(profile_id, include_relations=include_relations)

@router.get("/space-type/{space_type_id}")
def get_spaces_by_space_type(
    space_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Buscar espaços por tipo de espaço"""
    return space_service.get_spaces_by_space_type_id(space_type_id, include_relations=include_relations)

@router.get("/event-type/{event_type_id}")
def get_spaces_by_event_type(
    event_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Buscar espaços por tipo de evento"""
    return space_service.get_spaces_by_event_type_id(event_type_id, include_relations=include_relations)

@router.get("/festival-type/{festival_type_id}")
def get_spaces_by_festival_type(
    festival_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados"),
    space_service: SpaceService = Depends(get_space_service)
):
    """Buscar espaços por tipo de festival"""
    return space_service.get_spaces_by_festival_type_id(festival_type_id, include_relations=include_relations)

@router.put("/{space_id}", response_model=SpaceResponse)
def update_space(
    space_id: int,
    space: SpaceUpdate,
    space_service: SpaceService = Depends(get_space_service)
):
    """Atualizar um espaço"""
    try:
        # Usar model_dump e excluir campos None para atualização parcial
        space_data = space.model_dump(exclude_none=True)
        return space_service.update_space(space_id, space_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{space_id}", status_code=status.HTTP_200_OK)
def delete_space(
    space_id: int,
    space_service: SpaceService = Depends(get_space_service)
):
    """Deletar um espaço"""
    success = space_service.delete_space(space_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Space não encontrado"
        )
    return {"message": f"Space com ID {space_id} foi deletado com sucesso"} 