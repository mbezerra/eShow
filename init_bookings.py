#!/usr/bin/env python3
"""
Script para popular a tabela bookings com dados iniciais
seguindo as novas regras de negócio por role.

Regras:
- role_id = 1 (ADMIN): NUNCA faz agendamento
- role_id = 2 (ARTISTA): NUNCA agenda artist_id, apenas space_id/eventos/festivais  
- role_id = 3 (ESPACO): NUNCA agenda space_id, apenas artist_id/eventos/festivais
"""

from datetime import datetime, timedelta
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.booking_model import BookingModel
from infrastructure.database.models.profile_model import ProfileModel

def get_valid_profiles():
    """Obtém profiles válidos para agendamentos (role_id 2 e 3)"""
    session = SessionLocal()
    try:
        # Obter profiles artistas (role_id = 2) e espaços (role_id = 3)
        artist_profiles = session.query(ProfileModel).filter(ProfileModel.role_id == 2).limit(5).all()
        space_profiles = session.query(ProfileModel).filter(ProfileModel.role_id == 3).limit(5).all()
        return artist_profiles, space_profiles
    finally:
        session.close()

def init_bookings():
    session = SessionLocal()
    try:
        # Verificar se já existem bookings
        existing_count = session.query(BookingModel).count()
        if existing_count > 0:
            print(f"❌ Tabela bookings já possui {existing_count} registros")
            print("Execute o script de limpeza primeiro se necessário")
            return
        
        artist_profiles, space_profiles = get_valid_profiles()
        
        if not artist_profiles:
            print("❌ Nenhum profile com role ARTISTA encontrado")
            return
            
        if not space_profiles:
            print("❌ Nenhum profile com role ESPACO encontrado")
            return
        
        bookings_data = []
        base_date = datetime.now() + timedelta(days=30)  # Agendamentos futuros
        
        # 1. Agendamentos de ARTISTAS para ESPAÇOS (role_id = 2 agenda space_id)
        for i, artist_profile in enumerate(artist_profiles[:3]):
            booking_date = base_date + timedelta(days=i*7)
            bookings_data.append(BookingModel(
                profile_id=artist_profile.id,
                data_inicio=booking_date.replace(hour=20, minute=0, second=0),
                horario_inicio="20:00",
                data_fim=booking_date.replace(hour=23, minute=0, second=0),
                horario_fim="23:00",
                space_id=1,  # Artista agenda espaço
                artist_id=None,
                space_event_type_id=None,
                space_festival_type_id=None
            ))
        
        # 2. Agendamentos de ESPAÇOS para ARTISTAS (role_id = 3 agenda artist_id)
        for i, space_profile in enumerate(space_profiles[:3]):
            booking_date = base_date + timedelta(days=(i+3)*7)
            bookings_data.append(BookingModel(
                profile_id=space_profile.id,
                data_inicio=booking_date.replace(hour=19, minute=0, second=0),
                horario_inicio="19:00", 
                data_fim=booking_date.replace(hour=22, minute=0, second=0),
                horario_fim="22:00",
                space_id=None,
                artist_id=1,  # Espaço agenda artista
                space_event_type_id=None,
                space_festival_type_id=None
            ))
        
        # 3. Agendamentos de ARTISTAS para EVENTOS (role_id = 2 agenda space_event_type_id)
        if len(artist_profiles) > 3:
            for i, artist_profile in enumerate(artist_profiles[3:4]):
                booking_date = base_date + timedelta(days=(i+6)*7)
                bookings_data.append(BookingModel(
                    profile_id=artist_profile.id,
                    data_inicio=booking_date.replace(hour=18, minute=0, second=0),
                    horario_inicio="18:00",
                    data_fim=booking_date.replace(hour=23, minute=0, second=0),
                    horario_fim="23:00",
                    space_id=None,
                    artist_id=None,
                    space_event_type_id=1,  # Artista agenda evento
                    space_festival_type_id=None
                ))
        
        # 4. Agendamentos de ESPAÇOS para EVENTOS (role_id = 3 agenda space_event_type_id)
        if len(space_profiles) > 3:
            for i, space_profile in enumerate(space_profiles[3:4]):
                booking_date = base_date + timedelta(days=(i+7)*7)
                bookings_data.append(BookingModel(
                    profile_id=space_profile.id,
                    data_inicio=booking_date.replace(hour=17, minute=0, second=0),
                    horario_inicio="17:00",
                    data_fim=booking_date.replace(hour=21, minute=0, second=0),
                    horario_fim="21:00",
                    space_id=None,
                    artist_id=None,
                    space_event_type_id=2,  # Espaço agenda evento
                    space_festival_type_id=None
                ))
        
        # 5. Agendamentos de ARTISTAS para FESTIVAIS (role_id = 2 agenda space_festival_type_id)
        if len(artist_profiles) > 4:
            for i, artist_profile in enumerate(artist_profiles[4:5]):
                booking_date = base_date + timedelta(days=(i+8)*7)
                bookings_data.append(BookingModel(
                    profile_id=artist_profile.id,
                    data_inicio=booking_date.replace(hour=16, minute=0, second=0),
                    horario_inicio="16:00",
                    data_fim=booking_date.replace(hour=20, minute=0, second=0),
                    horario_fim="20:00",
                    space_id=None,
                    artist_id=None,
                    space_event_type_id=None,
                    space_festival_type_id=1  # Artista agenda festival
                ))
        
        # 6. Agendamentos de ESPAÇOS para FESTIVAIS (role_id = 3 agenda space_festival_type_id)
        if len(space_profiles) > 4:
            for i, space_profile in enumerate(space_profiles[4:5]):
                booking_date = base_date + timedelta(days=(i+9)*7)
                bookings_data.append(BookingModel(
                    profile_id=space_profile.id,
                    data_inicio=booking_date.replace(hour=15, minute=0, second=0),
                    horario_inicio="15:00",
                    data_fim=booking_date.replace(hour=19, minute=0, second=0),
                    horario_fim="19:00",
                    space_id=None,
                    artist_id=None,
                    space_event_type_id=None,
                    space_festival_type_id=2  # Espaço agenda festival
                ))
        
        # Inserir bookings
        session.add_all(bookings_data)
        session.commit()
        
        print(f"✅ {len(bookings_data)} agendamentos criados com sucesso!")
        print("\n🎯 DISTRIBUIÇÃO POR TIPO:")
        print(f"• Artistas agendando espaços: {len([b for b in bookings_data if b.space_id])}")
        print(f"• Espaços agendando artistas: {len([b for b in bookings_data if b.artist_id])}")
        print(f"• Agendamentos para eventos: {len([b for b in bookings_data if b.space_event_type_id])}")
        print(f"• Agendamentos para festivais: {len([b for b in bookings_data if b.space_festival_type_id])}")
        print("\n✅ REGRAS DE NEGÓCIO APLICADAS:")
        print("• ADMIN (role_id=1): Nenhum agendamento criado")
        print("• ARTISTA (role_id=2): Apenas agendamentos de espaços/eventos/festivais")
        print("• ESPACO (role_id=3): Apenas agendamentos de artistas/eventos/festivais")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar bookings: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("🔄 Inicializando bookings com novas regras de negócio...")
    init_bookings()
    print("✅ Inicialização concluída!") 