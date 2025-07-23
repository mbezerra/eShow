from typing import List, Optional, Union, Any
from datetime import datetime
from domain.repositories.booking_repository import BookingRepository
from domain.repositories.profile_repository import ProfileRepository
from domain.entities.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate

class BookingService:
    """Serviço de aplicação para agendamentos/reservas"""
    
    def __init__(self, booking_repository: BookingRepository, profile_repository: ProfileRepository):
        self.booking_repository = booking_repository
        self.profile_repository = profile_repository
    
    def create_booking(self, booking_data: BookingCreate) -> Booking:
        """Criar um novo agendamento"""
        
        # Validar regras de negócio por role
        profile = self.profile_repository.get_by_id(booking_data.profile_id)
        if not profile:
            raise ValueError(f"Profile com ID {booking_data.profile_id} não encontrado")
        
        # Regra 1: ADMIN (role_id = 1) NUNCA faz agendamento
        if profile.role_id == 1:
            raise ValueError("Usuários com role ADMIN não podem fazer agendamentos")
        
        # Regra 2: ARTISTA (role_id = 2) NUNCA agenda artist_id, apenas space_id
        elif profile.role_id == 2:
            if booking_data.artist_id is not None:
                raise ValueError("Usuários com role ARTISTA não podem agendar artistas, apenas espaços")
            if booking_data.space_id is None and booking_data.space_event_type_id is None and booking_data.space_festival_type_id is None:
                raise ValueError("Usuários com role ARTISTA devem agendar espaços, eventos ou festivais")
        
        # Regra 3: ESPACO (role_id = 3) NUNCA agenda space_id, apenas artist_id  
        elif profile.role_id == 3:
            if booking_data.space_id is not None:
                raise ValueError("Usuários com role ESPACO não podem agendar espaços, apenas artistas")
            if booking_data.artist_id is None and booking_data.space_event_type_id is None and booking_data.space_festival_type_id is None:
                raise ValueError("Usuários com role ESPACO devem agendar artistas, eventos ou festivais")
        
        booking = Booking(
            profile_id=booking_data.profile_id,
            data_inicio=booking_data.data_inicio,
            horario_inicio=booking_data.horario_inicio,
            data_fim=booking_data.data_fim,
            horario_fim=booking_data.horario_fim,
            space_id=booking_data.space_id,
            artist_id=booking_data.artist_id,
            space_event_type_id=booking_data.space_event_type_id,
            space_festival_type_id=booking_data.space_festival_type_id
        )
        
        return self.booking_repository.create(booking)
    
    def get_booking_by_id(self, booking_id: int, include_relations: bool = False) -> Optional[Union[Booking, Any]]:
        """Obter um agendamento por ID"""
        return self.booking_repository.get_by_id(booking_id, include_relations=include_relations)
    
    def get_bookings_by_profile(self, profile_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um profile"""
        return self.booking_repository.get_by_profile_id(profile_id, include_relations=include_relations)
    
    def get_bookings_by_space(self, space_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um espaço"""
        return self.booking_repository.get_by_space_id(space_id, include_relations=include_relations)
    
    def get_bookings_by_artist(self, artist_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um artista"""
        return self.booking_repository.get_by_artist_id(artist_id, include_relations=include_relations)
    
    def get_bookings_by_space_event_type(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um space-event type"""
        return self.booking_repository.get_by_space_event_type_id(space_event_type_id, include_relations=include_relations)
    
    def get_bookings_by_space_festival_type(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um space-festival type"""
        return self.booking_repository.get_by_space_festival_type_id(space_festival_type_id, include_relations=include_relations)
    
    def get_bookings_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter agendamentos em um período"""
        return self.booking_repository.get_by_date_range(data_inicio, data_fim, include_relations=include_relations)
    
    def update_booking(self, booking_id: int, booking_data: BookingUpdate) -> Optional[Booking]:
        """Atualizar um agendamento"""
        # Obter o agendamento atual
        existing = self.booking_repository.get_by_id(booking_id)
        if not existing:
            return None
        
        # Criar entidade com os dados atualizados
        updated_booking = Booking(
            id=existing.id,
            profile_id=existing.profile_id,  # Profile não pode ser alterado
            data_inicio=booking_data.data_inicio if booking_data.data_inicio is not None else existing.data_inicio,
            horario_inicio=booking_data.horario_inicio if booking_data.horario_inicio is not None else existing.horario_inicio,
            data_fim=booking_data.data_fim if booking_data.data_fim is not None else existing.data_fim,
            horario_fim=booking_data.horario_fim if booking_data.horario_fim is not None else existing.horario_fim,
            space_id=booking_data.space_id if booking_data.space_id is not None else existing.space_id,
            artist_id=booking_data.artist_id if booking_data.artist_id is not None else existing.artist_id,
            space_event_type_id=booking_data.space_event_type_id if booking_data.space_event_type_id is not None else existing.space_event_type_id,
            space_festival_type_id=booking_data.space_festival_type_id if booking_data.space_festival_type_id is not None else existing.space_festival_type_id,
            created_at=existing.created_at,
            updated_at=existing.updated_at
        )
        
        return self.booking_repository.update(booking_id, updated_booking)
    
    def delete_booking(self, booking_id: int) -> bool:
        """Deletar um agendamento"""
        return self.booking_repository.delete(booking_id)
    
    def get_all_bookings(self, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos"""
        return self.booking_repository.get_all(include_relations=include_relations) 