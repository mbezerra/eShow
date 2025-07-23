#!/usr/bin/env python3
"""
Script para inicializar a tabela bookings com dados de exemplo
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import SessionLocal
from infrastructure.database.models.booking_model import BookingModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.artist_model import ArtistModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel

def init_bookings():
    """Inicializar dados de exemplo para bookings"""
    db: Session = SessionLocal()
    
    try:
        # Verificar se já existem dados
        existing_count = db.query(BookingModel).count()
        if existing_count > 0:
            print(f"✅ Tabela bookings já possui {existing_count} registros")
            return
        
        # Obter dados existentes
        profiles = db.query(ProfileModel).limit(5).all()
        spaces = db.query(SpaceModel).limit(3).all()
        artists = db.query(ArtistModel).limit(3).all()
        space_event_types = db.query(SpaceEventTypeModel).limit(3).all()
        space_festival_types = db.query(SpaceFestivalTypeModel).limit(3).all()
        
        if not profiles:
            print("❌ Erro: Não há profiles cadastrados. Execute primeiro: python init_profiles.py")
            return
        
        # Dados de exemplo para agendamentos
        bookings_data = []
        
        # Agendamentos de espaços (artists contratando espaços)
        if spaces:
            bookings_data.extend([
                {
                    "profile_id": profiles[0].id,  # Profile de artista
                    "data_inicio": datetime(2025, 1, 15, 20, 0),
                    "horario_inicio": "20:00",
                    "data_fim": datetime(2025, 1, 15, 23, 0),
                    "horario_fim": "23:00",
                    "space_id": spaces[0].id,
                    "artist_id": None,
                    "space_event_type_id": None,
                    "space_festival_type_id": None
                },
                {
                    "profile_id": profiles[1].id,  # Profile de artista
                    "data_inicio": datetime(2025, 1, 20, 19, 0),
                    "horario_inicio": "19:00",
                    "data_fim": datetime(2025, 1, 20, 22, 30),
                    "horario_fim": "22:30",
                    "space_id": spaces[1].id if len(spaces) > 1 else spaces[0].id,
                    "artist_id": None,
                    "space_event_type_id": None,
                    "space_festival_type_id": None
                }
            ])
        
        # Agendamentos de artistas (spaces contratando artistas)
        if artists:
            bookings_data.extend([
                {
                    "profile_id": profiles[2].id,  # Profile de espaço
                    "data_inicio": datetime(2025, 1, 25, 21, 0),
                    "horario_inicio": "21:00",
                    "data_fim": datetime(2025, 1, 26, 1, 0),
                    "horario_fim": "01:00",
                    "space_id": None,
                    "artist_id": artists[0].id,
                    "space_event_type_id": None,
                    "space_festival_type_id": None
                },
                {
                    "profile_id": profiles[3].id,  # Profile de espaço
                    "data_inicio": datetime(2025, 2, 1, 18, 30),
                    "horario_inicio": "18:30",
                    "data_fim": datetime(2025, 2, 1, 23, 30),
                    "horario_fim": "23:30",
                    "space_id": None,
                    "artist_id": artists[1].id if len(artists) > 1 else artists[0].id,
                    "space_event_type_id": None,
                    "space_festival_type_id": None
                }
            ])
        
        # Agendamentos para eventos específicos
        if space_event_types:
            bookings_data.extend([
                {
                    "profile_id": profiles[0].id,
                    "data_inicio": datetime(2025, 2, 10, 20, 0),
                    "horario_inicio": "20:00",
                    "data_fim": datetime(2025, 2, 11, 2, 0),
                    "horario_fim": "02:00",
                    "space_id": None,
                    "artist_id": None,
                    "space_event_type_id": space_event_types[0].id,
                    "space_festival_type_id": None
                },
                {
                    "profile_id": profiles[1].id,
                    "data_inicio": datetime(2025, 2, 14, 19, 0),
                    "horario_inicio": "19:00",
                    "data_fim": datetime(2025, 2, 14, 23, 0),
                    "horario_fim": "23:00",
                    "space_id": None,
                    "artist_id": None,
                    "space_event_type_id": space_event_types[1].id if len(space_event_types) > 1 else space_event_types[0].id,
                    "space_festival_type_id": None
                }
            ])
        
        # Agendamentos para festivais específicos
        if space_festival_types:
            bookings_data.extend([
                {
                    "profile_id": profiles[2].id,
                    "data_inicio": datetime(2025, 3, 5, 18, 0),
                    "horario_inicio": "18:00",
                    "data_fim": datetime(2025, 3, 6, 4, 0),
                    "horario_fim": "04:00",
                    "space_id": None,
                    "artist_id": None,
                    "space_event_type_id": None,
                    "space_festival_type_id": space_festival_types[0].id
                },
                {
                    "profile_id": profiles[3].id,
                    "data_inicio": datetime(2025, 3, 15, 17, 30),
                    "horario_inicio": "17:30",
                    "data_fim": datetime(2025, 3, 16, 2, 30),
                    "horario_fim": "02:30",
                    "space_id": None,
                    "artist_id": None,
                    "space_event_type_id": None,
                    "space_festival_type_id": space_festival_types[1].id if len(space_festival_types) > 1 else space_festival_types[0].id
                }
            ])
        
        # Agendamentos adicionais para demonstrar variedade
        bookings_data.extend([
            {
                "profile_id": profiles[4].id if len(profiles) > 4 else profiles[0].id,
                "data_inicio": datetime(2025, 3, 22, 16, 0),
                "horario_inicio": "16:00",
                "data_fim": datetime(2025, 3, 22, 20, 0),
                "horario_fim": "20:00",
                "space_id": spaces[2].id if len(spaces) > 2 else spaces[0].id,
                "artist_id": None,
                "space_event_type_id": None,
                "space_festival_type_id": None
            },
            {
                "profile_id": profiles[0].id,
                "data_inicio": datetime(2025, 4, 1, 21, 30),
                "horario_inicio": "21:30",
                "data_fim": datetime(2025, 4, 2, 1, 30),
                "horario_fim": "01:30",
                "space_id": None,
                "artist_id": artists[2].id if len(artists) > 2 else artists[0].id,
                "space_event_type_id": None,
                "space_festival_type_id": None
            }
        ])
        
        # Criar os agendamentos
        bookings = []
        for data in bookings_data:
            booking = BookingModel(**data)
            bookings.append(booking)
        
        # Adicionar todos de uma vez
        db.add_all(bookings)
        db.commit()
        
        print(f"✅ Inseridos {len(bookings)} agendamentos com sucesso!")
        
        # Mostrar alguns exemplos inseridos
        print("\n📋 EXEMPLOS DE AGENDAMENTOS CRIADOS:")
        for i, booking in enumerate(bookings[:3], 1):
            profile_id = booking.profile_id
            tipo_agendamento = ""
            if booking.space_id:
                tipo_agendamento = f"Espaço ID {booking.space_id}"
            elif booking.artist_id:
                tipo_agendamento = f"Artista ID {booking.artist_id}"
            elif booking.space_event_type_id:
                tipo_agendamento = f"Evento ID {booking.space_event_type_id}"
            elif booking.space_festival_type_id:
                tipo_agendamento = f"Festival ID {booking.space_festival_type_id}"
            
            print(f"   {i}. Profile {profile_id} - {tipo_agendamento}: {booking.data_inicio.strftime('%d/%m/%Y')} {booking.horario_inicio}")
        
        if len(bookings) > 3:
            print(f"   ... e mais {len(bookings) - 3} agendamentos!")
            
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        db.rollback()
        raise
        
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando dados da tabela bookings...")
    init_bookings()
    print("✅ Script concluído!") 