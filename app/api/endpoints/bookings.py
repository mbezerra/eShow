from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from app.schemas.booking import (
    BookingCreate, 
    BookingUpdate,
    BookingResponse, 
    BookingListResponse
)
from app.application.services.booking_service import BookingService
from app.application.dependencies import get_booking_service
from app.core.auth import get_current_active_user
from app.schemas.user import UserResponse

def convert_booking_to_response(booking):
    """Converter agendamento para o schema de resposta"""
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

def convert_bookings_list_to_response(bookings):
    """Converter lista de agendamentos para o schema de resposta"""
    converted_items = [convert_booking_to_response(item) for item in bookings]
    return BookingListResponse(items=converted_items)

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

@router.get("/", response_model=BookingListResponse)
def get_all_bookings(
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos (requer autenticação)"""
    bookings = booking_service.get_all_bookings()
    return convert_bookings_list_to_response(bookings)

@router.get("/profile/{profile_id}", response_model=BookingListResponse)
def get_bookings_by_profile(
    profile_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um profile (requer autenticação)"""
    bookings = booking_service.get_bookings_by_profile(profile_id)
    return convert_bookings_list_to_response(bookings)

@router.get("/space/{space_id}", response_model=BookingListResponse)
def get_bookings_by_space(
    space_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um espaço (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space(space_id)
    return convert_bookings_list_to_response(bookings)

@router.get("/artist/{artist_id}", response_model=BookingListResponse)
def get_bookings_by_artist(
    artist_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um artista (requer autenticação)"""
    bookings = booking_service.get_bookings_by_artist(artist_id)
    return convert_bookings_list_to_response(bookings)

@router.get("/space-event-type/{space_event_type_id}", response_model=BookingListResponse)
def get_bookings_by_space_event_type(
    space_event_type_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um space-event type (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space_event_type(space_event_type_id)
    return convert_bookings_list_to_response(bookings)

@router.get("/space-festival-type/{space_festival_type_id}", response_model=BookingListResponse)
def get_bookings_by_space_festival_type(
    space_festival_type_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter todos os agendamentos de um space-festival type (requer autenticação)"""
    bookings = booking_service.get_bookings_by_space_festival_type(space_festival_type_id)
    return convert_bookings_list_to_response(bookings)

@router.get("/date-range", response_model=BookingListResponse)
def get_bookings_by_date_range(
    data_inicio: datetime = Query(..., description="Data de início (ISO format)"),
    data_fim: datetime = Query(..., description="Data de fim (ISO format)"),
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter agendamentos em um período (requer autenticação)"""
    if data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de fim deve ser posterior à data de início"
        )
    
    bookings = booking_service.get_bookings_by_date_range(data_inicio, data_fim)
    return convert_bookings_list_to_response(bookings)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    booking_service: BookingService = Depends(get_booking_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obter um agendamento por ID (requer autenticação)"""
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
    
    return convert_booking_to_response(booking)

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