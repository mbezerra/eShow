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
    print("🚀 Inicializando dados de exemplo para Artists...")
    
    # Obter sessão do banco
    session = next(get_database_session())
    artist_repository = ArtistRepositoryImpl(session)
    
    # Dados de exemplo
    artists_data = [
        {
            "profile_id": 1,  # Assumindo que existe um profile com ID 1
            "artist_type_id": 1,  # Cantor(a) solo
            "dias_apresentacao": ["sexta", "sábado", "domingo"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 150.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico, microfone, iluminação adequada",
            "instagram": "https://instagram.com/artista1",
            "youtube": "https://youtube.com/@artista1",
            "spotify": "https://open.spotify.com/artist/artista1"
        },
        {
            "profile_id": 2,  # Assumindo que existe um profile com ID 2
            "artist_type_id": 4,  # Banda
            "dias_apresentacao": ["quinta", "sexta", "sábado"],
            "raio_atuacao": 100.0,
            "duracao_apresentacao": 3.0,
            "valor_hora": 300.0,
            "valor_couvert": 30.0,
            "requisitos_minimos": "Palco mínimo 4x3m, sistema de som completo, bateria, amplificadores",
            "instagram": "https://instagram.com/banda1",
            "facebook": "https://facebook.com/banda1",
            "soundcloud": "https://soundcloud.com/banda1"
        },
        {
            "profile_id": 3,  # Assumindo que existe um profile com ID 3
            "artist_type_id": 2,  # Dupla
            "dias_apresentacao": ["segunda", "terça", "quarta", "quinta", "sexta"],
            "raio_atuacao": 30.0,
            "duracao_apresentacao": 1.5,
            "valor_hora": 120.0,
            "valor_couvert": 15.0,
            "requisitos_minimos": "Dois microfones, violão, sistema de som simples",
            "tiktok": "https://tiktok.com/@dupla1",
            "youtube": "https://youtube.com/@dupla1"
        }
    ]
    
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