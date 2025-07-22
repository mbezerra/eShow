from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dependencies import get_space_type_service
from app.application.services.space_type_service import SpaceTypeService
from app.schemas.space_type import SpaceTypeCreate, SpaceTypeUpdate, SpaceTypeResponse

router = APIRouter()

@router.post("/", response_model=SpaceTypeResponse, status_code=status.HTTP_201_CREATED)
def create_space_type(
    space_type: SpaceTypeCreate,
    space_type_service: SpaceTypeService = Depends(get_space_type_service)
):
    """Criar um novo tipo de espaço"""
    try:
        created_space_type = space_type_service.create_space_type(space_type.tipo)
        return SpaceTypeResponse(
            id=created_space_type.id,
            tipo=created_space_type.tipo,
            created_at=created_space_type.created_at,
            updated_at=created_space_type.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{space_type_id}", response_model=SpaceTypeResponse)
def get_space_type(
    space_type_id: int,
    space_type_service: SpaceTypeService = Depends(get_space_type_service)
):
    """Obter um tipo de espaço por ID"""
    space_type = space_type_service.get_space_type_by_id(space_type_id)
    if not space_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SpaceType não encontrado"
        )
    return SpaceTypeResponse(
        id=space_type.id,
        tipo=space_type.tipo,
        created_at=space_type.created_at,
        updated_at=space_type.updated_at
    )

@router.get("/", response_model=List[SpaceTypeResponse])
def get_all_space_types(
    skip: int = 0,
    limit: int = 100,
    space_type_service: SpaceTypeService = Depends(get_space_type_service)
):
    """Listar todos os tipos de espaço"""
    space_types = space_type_service.get_all_space_types(skip=skip, limit=limit)
    return [
        SpaceTypeResponse(
            id=space_type.id,
            tipo=space_type.tipo,
            created_at=space_type.created_at,
            updated_at=space_type.updated_at
        )
        for space_type in space_types
    ]

@router.put("/{space_type_id}", response_model=SpaceTypeResponse)
def update_space_type(
    space_type_id: int,
    space_type_update: SpaceTypeUpdate,
    space_type_service: SpaceTypeService = Depends(get_space_type_service)
):
    """Atualizar um tipo de espaço"""
    try:
        updated_space_type = space_type_service.update_space_type(space_type_id, space_type_update.tipo)
        return SpaceTypeResponse(
            id=updated_space_type.id,
            tipo=updated_space_type.tipo,
            created_at=updated_space_type.created_at,
            updated_at=updated_space_type.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{space_type_id}", status_code=status.HTTP_200_OK)
def delete_space_type(
    space_type_id: int,
    space_type_service: SpaceTypeService = Depends(get_space_type_service)
):
    """Deletar um tipo de espaço"""
    success = space_type_service.delete_space_type(space_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SpaceType não encontrado"
        )
    return {"message": f"SpaceType com ID {space_type_id} foi deletado com sucesso"} 