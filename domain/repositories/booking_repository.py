from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
from datetime import datetime
from domain.entities.booking import Booking

class BookingRepository(ABC):
    """Interface do repositório para agendamentos/reservas"""
    
    @abstractmethod
    def create(self, booking: Booking) -> Booking:
        """Criar um novo agendamento"""
        pass
    
    @abstractmethod
    def get_by_id(self, booking_id: int, include_relations: bool = False) -> Optional[Union[Booking, Any]]:
        """Obter um agendamento por ID"""
        pass
    
    @abstractmethod
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um profile"""
        pass
    
    @abstractmethod
    def get_by_space_id(self, space_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um espaço"""
        pass
    
    @abstractmethod
    def get_by_artist_id(self, artist_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um artista"""
        pass
    
    @abstractmethod
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um space-event type"""
        pass
    
    @abstractmethod
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos de um space-festival type"""
        pass
    
    @abstractmethod
    def get_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter agendamentos em um período"""
        pass
    
    @abstractmethod
    def update(self, booking_id: int, booking: Booking) -> Optional[Booking]:
        """Atualizar um agendamento"""
        pass
    
    @abstractmethod
    def delete(self, booking_id: int) -> bool:
        """Deletar um agendamento"""
        pass
    
    @abstractmethod
    def get_all(self, include_relations: bool = False) -> List[Union[Booking, Any]]:
        """Obter todos os agendamentos"""
        pass 