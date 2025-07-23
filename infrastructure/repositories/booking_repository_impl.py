from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from domain.repositories.booking_repository import BookingRepository
from domain.entities.booking import Booking
from infrastructure.database.models.booking_model import BookingModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.artist_model import ArtistModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel

class BookingRepositoryImpl(BookingRepository):
    """Implementação do repositório para agendamentos/reservas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _configure_relations(self, query, include_relations: bool = False):
        """Configurar relacionamentos para a query"""
        if include_relations:
            query = query.options(
                joinedload(BookingModel.profile),
                joinedload(BookingModel.space),
                joinedload(BookingModel.artist),
                joinedload(BookingModel.space_event_type),
                joinedload(BookingModel.space_festival_type)
            )
        return query
    
    def create(self, booking: Booking) -> Booking:
        """Criar um novo agendamento"""
        # Verificar se o profile existe
        profile = self.db.query(ProfileModel).filter(ProfileModel.id == booking.profile_id).first()
        if not profile:
            raise ValueError(f"Profile com ID {booking.profile_id} não encontrado")
        
        # Verificar se os relacionamentos existem quando especificados
        if booking.space_id:
            space = self.db.query(SpaceModel).filter(SpaceModel.id == booking.space_id).first()
            if not space:
                raise ValueError(f"Espaço com ID {booking.space_id} não encontrado")
        
        if booking.artist_id:
            artist = self.db.query(ArtistModel).filter(ArtistModel.id == booking.artist_id).first()
            if not artist:
                raise ValueError(f"Artista com ID {booking.artist_id} não encontrado")
        
        if booking.space_event_type_id:
            space_event_type = self.db.query(SpaceEventTypeModel).filter(SpaceEventTypeModel.id == booking.space_event_type_id).first()
            if not space_event_type:
                raise ValueError(f"Space-Event Type com ID {booking.space_event_type_id} não encontrado")
        
        if booking.space_festival_type_id:
            space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(SpaceFestivalTypeModel.id == booking.space_festival_type_id).first()
            if not space_festival_type:
                raise ValueError(f"Space-Festival Type com ID {booking.space_festival_type_id} não encontrado")
        
        # Criar o agendamento
        db_booking = BookingModel(
            profile_id=booking.profile_id,
            data_inicio=booking.data_inicio,
            horario_inicio=booking.horario_inicio,
            data_fim=booking.data_fim,
            horario_fim=booking.horario_fim,
            space_id=booking.space_id,
            artist_id=booking.artist_id,
            space_event_type_id=booking.space_event_type_id,
            space_festival_type_id=booking.space_festival_type_id
        )
        
        self.db.add(db_booking)
        self.db.commit()
        self.db.refresh(db_booking)
        
        return self._to_entity(db_booking)
    
    def get_by_id(self, booking_id: int, include_relations: bool = False) -> Optional[Union[Booking, BookingModel]]:
        """Obter um agendamento por ID"""
        query = self.db.query(BookingModel).filter(BookingModel.id == booking_id)
        query = self._configure_relations(query, include_relations)
        booking = query.first()
        
        if not booking:
            return None
        
        if include_relations:
            return booking  # Retorna o modelo com relacionamentos carregados
        return self._to_entity(booking)
    
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos de um profile"""
        query = self.db.query(BookingModel).filter(BookingModel.profile_id == profile_id)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def get_by_space_id(self, space_id: int, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos de um espaço"""
        query = self.db.query(BookingModel).filter(BookingModel.space_id == space_id)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def get_by_artist_id(self, artist_id: int, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos de um artista"""
        query = self.db.query(BookingModel).filter(BookingModel.artist_id == artist_id)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos de um space-event type"""
        query = self.db.query(BookingModel).filter(BookingModel.space_event_type_id == space_event_type_id)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos de um space-festival type"""
        query = self.db.query(BookingModel).filter(BookingModel.space_festival_type_id == space_festival_type_id)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def get_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter agendamentos em um período"""
        query = self.db.query(BookingModel).filter(
            BookingModel.data_inicio >= data_inicio,
            BookingModel.data_fim <= data_fim
        )
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def update(self, booking_id: int, booking: Booking) -> Optional[Booking]:
        """Atualizar um agendamento"""
        db_booking = self.db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        
        if not db_booking:
            return None
        
        # Verificar relacionamentos se foram alterados
        if booking.space_id and booking.space_id != db_booking.space_id:
            space = self.db.query(SpaceModel).filter(SpaceModel.id == booking.space_id).first()
            if not space:
                raise ValueError(f"Espaço com ID {booking.space_id} não encontrado")
        
        if booking.artist_id and booking.artist_id != db_booking.artist_id:
            artist = self.db.query(ArtistModel).filter(ArtistModel.id == booking.artist_id).first()
            if not artist:
                raise ValueError(f"Artista com ID {booking.artist_id} não encontrado")
        
        if booking.space_event_type_id and booking.space_event_type_id != db_booking.space_event_type_id:
            space_event_type = self.db.query(SpaceEventTypeModel).filter(SpaceEventTypeModel.id == booking.space_event_type_id).first()
            if not space_event_type:
                raise ValueError(f"Space-Event Type com ID {booking.space_event_type_id} não encontrado")
        
        if booking.space_festival_type_id and booking.space_festival_type_id != db_booking.space_festival_type_id:
            space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(SpaceFestivalTypeModel.id == booking.space_festival_type_id).first()
            if not space_festival_type:
                raise ValueError(f"Space-Festival Type com ID {booking.space_festival_type_id} não encontrado")
        
        # Atualizar os campos
        if booking.data_inicio:
            db_booking.data_inicio = booking.data_inicio
        if booking.horario_inicio:
            db_booking.horario_inicio = booking.horario_inicio
        if booking.data_fim:
            db_booking.data_fim = booking.data_fim
        if booking.horario_fim:
            db_booking.horario_fim = booking.horario_fim
        if booking.space_id is not None:
            db_booking.space_id = booking.space_id
        if booking.artist_id is not None:
            db_booking.artist_id = booking.artist_id
        if booking.space_event_type_id is not None:
            db_booking.space_event_type_id = booking.space_event_type_id
        if booking.space_festival_type_id is not None:
            db_booking.space_festival_type_id = booking.space_festival_type_id
        
        self.db.commit()
        self.db.refresh(db_booking)
        
        return self._to_entity(db_booking)
    
    def delete(self, booking_id: int) -> bool:
        """Deletar um agendamento"""
        booking = self.db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        
        if not booking:
            return False
        
        self.db.delete(booking)
        self.db.commit()
        return True
    
    def get_all(self, include_relations: bool = False) -> List[Union[Booking, BookingModel]]:
        """Obter todos os agendamentos"""
        query = self.db.query(BookingModel)
        query = self._configure_relations(query, include_relations)
        bookings = query.all()
        
        if include_relations:
            return bookings  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(booking) for booking in bookings]
    
    def _to_entity(self, model: BookingModel) -> Booking:
        """Converter modelo para entidade"""
        return Booking(
            id=model.id,
            profile_id=model.profile_id,
            data_inicio=model.data_inicio,
            horario_inicio=model.horario_inicio,
            data_fim=model.data_fim,
            horario_fim=model.horario_fim,
            space_id=model.space_id,
            artist_id=model.artist_id,
            space_event_type_id=model.space_event_type_id,
            space_festival_type_id=model.space_festival_type_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 