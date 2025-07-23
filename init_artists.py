#!/usr/bin/env python3
"""
Script para inicializar dados de exemplo para Artists
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import get_database_session
from infrastructure.repositories.artist_repository_impl import ArtistRepositoryImpl
from domain.entities.artist import Artist

def init_artists():
    """Inicializar dados de exemplo para artists"""
    from infrastructure.database.models.profile_model import ProfileModel
    
    print("🚀 Inicializando dados de exemplo para Artists...")
    
    # Obter sessão do banco
    session = next(get_database_session())
    artist_repository = ArtistRepositoryImpl(session)
    
    # Buscar apenas profiles com role_id = 2 (ARTISTA)
    artist_profiles = session.query(ProfileModel).filter_by(role_id=2).all()
    
    if not artist_profiles:
        print("❌ Nenhum profile com role 'ARTISTA' encontrado. Execute primeiro os scripts de usuários e profiles.")
        return
    
    print(f"📍 Encontrados {len(artist_profiles)} profiles com role ARTISTA")
    
    # Dados de exemplo usando profiles válidos
    artists_data = [
        {
            "profile_id": artist_profiles[0].id,  # Bruno Show
            "artist_type_id": 1,  # Cantor(a) solo
            "dias_apresentacao": ["sexta", "sábado", "domingo"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 150.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico, microfone, iluminação adequada",
            "instagram": "https://instagram.com/bruno_show",
            "youtube": "https://youtube.com/@bruno_show",
            "spotify": "https://open.spotify.com/artist/bruno_show"
        }
    ]
    
    # Adicionar mais artists se temos mais profiles
    if len(artist_profiles) > 1:
        artists_data.append({
            "profile_id": artist_profiles[1].id,  # Ana Costa Music
            "artist_type_id": 1,  # Cantor(a) solo
            "dias_apresentacao": ["quinta", "sexta", "sábado"],
            "raio_atuacao": 80.0,
            "duracao_apresentacao": 2.5,
            "valor_hora": 200.0,
            "valor_couvert": 25.0,
            "requisitos_minimos": "Piano ou teclado, sistema de som de qualidade, microfone condensador",
            "instagram": "https://instagram.com/ana_costa_music",
            "youtube": "https://youtube.com/@ana_costa_music",
            "spotify": "https://open.spotify.com/artist/ana_costa"
        })
        
    if len(artist_profiles) > 2:
        artists_data.append({
            "profile_id": artist_profiles[2].id,  # Diego Rock
            "artist_type_id": 4,  # Banda
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 120.0,
            "duracao_apresentacao": 3.0,
            "valor_hora": 300.0,
            "valor_couvert": 35.0,
            "requisitos_minimos": "Palco mínimo 4x3m, sistema de som completo, bateria, amplificadores",
            "instagram": "https://instagram.com/diego_rock",
            "facebook": "https://facebook.com/diego_rock",
            "soundcloud": "https://soundcloud.com/diego_rock"
        })
        
    if len(artist_profiles) > 3:
        artists_data.append({
            "profile_id": artist_profiles[3].id,  # Elena Jazz
            "artist_type_id": 1,  # Cantor(a) solo
            "dias_apresentacao": ["quinta", "sexta", "sábado", "domingo"],
            "raio_atuacao": 60.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 180.0,
            "valor_couvert": 30.0,
            "requisitos_minimos": "Piano acústico ou elétrico, sistema de som jazz, microfone vintage",
            "instagram": "https://instagram.com/elena_jazz",
            "youtube": "https://youtube.com/@elena_jazz",
            "spotify": "https://open.spotify.com/artist/elena_jazz",
            "deezer": "https://deezer.com/artist/elena_jazz"
        })
    
    try:
        for artist_data in artists_data:
            # Verificar se já existe um artista para este profile
            existing_artist = artist_repository.get_by_profile_id(artist_data["profile_id"])
            if existing_artist:
                print(f"⚠️  Artista já existe para o profile {artist_data['profile_id']}")
                continue
            
            # Criar artista
            artist = Artist(**artist_data)
            created_artist = artist_repository.create(artist)
            print(f"✅ Artista criado com ID: {created_artist.id} para profile {created_artist.profile_id}")
        
        print("🎉 Inicialização de Artists concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar artists: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_artists() 