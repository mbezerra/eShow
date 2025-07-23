from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Union
from datetime import datetime
from app.schemas.booking import (
    BookingCreate, 
    BookingUpdate,
    BookingResponse, 
    BookingListResponse,
    BookingWithRelations,
    BookingListWithRelations
)
from app.application.services.booking_service import BookingService
from app.application.dependencies import get_booking_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_booking_to_response(booking, include_relations: bool = False):
    """Converter agendamento para o schema de resposta apropriado"""
    if include_relations:
        # Se include_relations=True, booking pode ser um BookingModel
        from infrastructure.database.models.booking_model import BookingModel
        if isinstance(booking, BookingModel):
            # Converter o modelo do banco para o schema com relacionamentos
            return BookingWithRelations.model_validate({
                "id": booking.id,
                "profile_id": booking.profile_id,
                "data_inicio": booking.data_inicio,
                "horario_inicio": booking.horario_inicio,
                "data_fim": booking.data_fim,
                "horario_fim": booking.horario_fim,
                "space_id": booking.space_id,
                "artist_id": booking.artist_id,
                "space_event_type_id": booking.space_event_type_id,
                "space_festival_type_id": booking.space_festival_type_id,
                "created_at": booking.created_at,
                "updated_at": booking.updated_at,
                "profile": booking.profile,
                "space": booking.space,
                "artist": booking.artist,
                "space_event_type": booking.space_event_type,
                "space_festival_type": booking.space_festival_type
            })
        else:
            return BookingWithRelations.model_validate(booking)
    else:
        return BookingResponse.model_validate({
            "id": booking.id,
            "profile_id": booking.profile_id,
            "data_inicio": booking.data_inicio,
            "horario_inicio": booking.horario_inicio,
            "data_fim": booking.data_fim,
            "horario_fim": booking.horario_fim,
            "space_id": booking.space_id,
            "artist_id": booking.artist_id,
            "space_event_type_id": booking.space_event_type_id,
            "space_festival_type_id": booking.space_festival_type_id,
            "created_at": booking.created_at,
            "updated_at": booking.updated_at
        })

def convert_bookings_list_to_response(bookings, include_relations: bool = False):
    """Converter lista de agendamentos para o schema de resposta apropriado"""
    converted_bookings = [convert_booking_to_response(booking, include_relations) for booking in bookings]
    if include_relations:
        return BookingListWithRelations(items=converted_bookings)
    else:
        return BookingListResponse(items=converted_bookings)

router = APIRouter()

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Criar um novo agendamento (requer autenticação)"""
    try:
        booking = booking_service.create_booking(booking_data)
        return convert_booking_to_response(booking)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/")
def get_all_bookings(
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos (requer autenticação)"""
    bookings = booking_service.get_all_bookings(include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/profile/{profile_id}")
def get_bookings_by_profile(
    profile_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um profile (requer autenticação)"""
    bookings = booking_service.get_bookings_by_profile(profile_id, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/space/{space_id}")
def get_bookings_by_space(
    space_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um espaço (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space(space_id, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/artist/{artist_id}")
def get_bookings_by_artist(
    artist_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um artista (requer autenticação)"""
    bookings = booking_service.get_bookings_by_artist(artist_id, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/space-event-type/{space_event_type_id}")
def get_bookings_by_space_event_type(
    space_event_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um space-event type (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space_event_type(space_event_type_id, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/space-festival-type/{space_festival_type_id}")
def get_bookings_by_space_festival_type(
    space_festival_type_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um space-festival type (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space_festival_type(space_festival_type_id, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/date-range")
def get_bookings_by_date_range(
    data_inicio: datetime = Query(..., description="Data de início (ISO format)"),
    data_fim: datetime = Query(..., description="Data de fim (ISO format)"),
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter agendamentos em um período (requer autenticação)"""
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de fim deve ser posterior à data de início"
        )
    
    bookings = booking_service.get_bookings_by_date_range(data_inicio, data_fim, include_relations=include_relations)
    return convert_bookings_list_to_response(bookings, include_relations=include_relations)

@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    include_relations: bool = Query(False, description="Incluir dados relacionados (profile, space, artist)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um agendamento por ID (requer autenticação)"""
    booking = booking_service.get_booking_by_id(booking_id, include_relations=include_relations)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    return convert_booking_to_response(booking, include_relations=include_relations)

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar um agendamento (requer autenticação)"""
    try:
        booking = booking_service.update_booking(booking_id, booking_data)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento não encontrado"
            )
        return convert_booking_to_response(booking)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(
    booking_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Deletar um agendamento (requer autenticação)"""
    success = booking_service.delete_booking(booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    return {"message": f"Agendamento {booking_id} foi deletado com sucesso"} 