from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.festival_type import FestivalTypeCreate, FestivalTypeUpdate, FestivalTypeResponse
from app.application.services.festival_type_service import FestivalTypeService
from app.application.dependencies import get_festival_type_service

router = APIRouter()

@router.post("/", response_model=FestivalTypeResponse, status_code=status.HTTP_201_CREATED)
def create_festival_type(
    festival_type: FestivalTypeCreate,
    festival_type_service: FestivalTypeService = Depends(get_festival_type_service)
):
    """Criar um novo tipo de festival"""
    try:
        return festival_type_service.create_festival_type(festival_type.type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[FestivalTypeResponse])
def get_festival_types(
    skip: int = 0,
    limit: int = 100,
    festival_type_service: FestivalTypeService = Depends(get_festival_type_service)
):
    """Listar todos os tipos de festival"""
    return festival_type_service.get_all_festival_types(skip=skip, limit=limit)

@router.get("/{festival_type_id}", response_model=FestivalTypeResponse)
def get_festival_type(
    festival_type_id: int,
    festival_type_service: FestivalTypeService = Depends(get_festival_type_service)
):
    """Buscar um tipo de festival por ID"""
    festival_type = festival_type_service.get_festival_type_by_id(festival_type_id)
    if not festival_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FestivalType não encontrado"
        )
    return festival_type

@router.put("/{festival_type_id}", response_model=FestivalTypeResponse)
def update_festival_type(
    festival_type_id: int,
    festival_type: FestivalTypeUpdate,
    festival_type_service: FestivalTypeService = Depends(get_festival_type_service)
):
    """Atualizar um tipo de festival"""
    try:
        return festival_type_service.update_festival_type(festival_type_id, festival_type.type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{festival_type_id}", status_code=status.HTTP_200_OK)
def delete_festival_type(
    festival_type_id: int,
    festival_type_service: FestivalTypeService = Depends(get_festival_type_service)
):
    """Deletar um tipo de festival"""
    success = festival_type_service.delete_festival_type(festival_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FestivalType não encontrado"
        )
    return {"message": f"FestivalType com ID {festival_type_id} foi deletado com sucesso"} 