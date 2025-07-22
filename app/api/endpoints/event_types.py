from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dependencies import get_event_type_service
from app.application.services.event_type_service import EventTypeService
from app.schemas.event_type import EventTypeCreate, EventTypeUpdate, EventTypeResponse

router = APIRouter()

@router.post("/", response_model=EventTypeResponse, status_code=status.HTTP_201_CREATED)
def create_event_type(
    event_type: EventTypeCreate,
    event_type_service: EventTypeService = Depends(get_event_type_service)
):
    """Criar um novo tipo de evento"""
    try:
        created_event_type = event_type_service.create_event_type(event_type.type)
        return EventTypeResponse(
            id=created_event_type.id,
            type=created_event_type.type,
            created_at=created_event_type.created_at,
            updated_at=created_event_type.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{event_type_id}", response_model=EventTypeResponse)
def get_event_type(
    event_type_id: int,
    event_type_service: EventTypeService = Depends(get_event_type_service)
):
    """Obter um tipo de evento por ID"""
    event_type = event_type_service.get_event_type_by_id(event_type_id)
    if not event_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EventType não encontrado"
        )
    return EventTypeResponse(
        id=event_type.id,
        type=event_type.type,
        created_at=event_type.created_at,
        updated_at=event_type.updated_at
    )

@router.get("/", response_model=List[EventTypeResponse])
def get_all_event_types(
    skip: int = 0,
    limit: int = 100,
    event_type_service: EventTypeService = Depends(get_event_type_service)
):
    """Listar todos os tipos de evento"""
    event_types = event_type_service.get_all_event_types(skip=skip, limit=limit)
    return [
        EventTypeResponse(
            id=event_type.id,
            type=event_type.type,
            created_at=event_type.created_at,
            updated_at=event_type.updated_at
        )
        for event_type in event_types
    ]

@router.put("/{event_type_id}", response_model=EventTypeResponse)
def update_event_type(
    event_type_id: int,
    event_type_update: EventTypeUpdate,
    event_type_service: EventTypeService = Depends(get_event_type_service)
):
    """Atualizar um tipo de evento"""
    try:
        updated_event_type = event_type_service.update_event_type(event_type_id, event_type_update.type)
        return EventTypeResponse(
            id=updated_event_type.id,
            type=updated_event_type.type,
            created_at=updated_event_type.created_at,
            updated_at=updated_event_type.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{event_type_id}", status_code=status.HTTP_200_OK)
def delete_event_type(
    event_type_id: int,
    event_type_service: EventTypeService = Depends(get_event_type_service)
):
    """Deletar um tipo de evento"""
    success = event_type_service.delete_event_type(event_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EventType não encontrado"
        )
    return {"message": f"EventType com ID {event_type_id} foi deletado com sucesso"} 