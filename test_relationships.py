#!/usr/bin/env python3
"""
Script para testar os relacionamentos entre as tabelas artists, profiles e artist_types
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import get_database_session
from infrastructure.repositories.artist_repository_impl import ArtistRepositoryImpl
from infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from infrastructure.repositories.artist_type_repository_impl import ArtistTypeRepositoryImpl

def test_relationships():
    """Testar os relacionamentos entre as tabelas"""
    print("🔍 Testando relacionamentos entre tabelas...")
    
    # Obter sessão do banco
    session = next(get_database_session())
    
    try:
        # Repositórios
        artist_repo = ArtistRepositoryImpl(session)
        profile_repo = ProfileRepositoryImpl(session)
        artist_type_repo = ArtistTypeRepositoryImpl(session)
        
        # 1. Verificar se existem dados nas tabelas relacionadas
        print("\n1. Verificando dados nas tabelas relacionadas...")
        
        profiles = profile_repo.get_all()
        print(f"   📊 Profiles encontrados: {len(profiles)}")
        for profile in profiles[:3]:  # Mostrar apenas os primeiros 3
            print(f"      - ID: {profile.id}, Nome: {profile.full_name}")
        
        artist_types = artist_type_repo.get_all()
        print(f"   📊 Artist Types encontrados: {len(artist_types)}")
        for artist_type in artist_types:
            print(f"      - ID: {artist_type.id}, Tipo: {artist_type.tipo}")
        
        # 2. Verificar artistas existentes
        artists = artist_repo.get_all()
        print(f"\n2. Artists encontrados: {len(artists)}")
        
        if artists:
            for artist in artists:
                print(f"   🎭 Artist ID: {artist.id}")
                print(f"      - Profile ID: {artist.profile_id}")
                print(f"      - Artist Type ID: {artist.artist_type_id}")
                print(f"      - Dias: {artist.dias_apresentacao}")
                print(f"      - Valor/hora: R$ {artist.valor_hora}")
                print()
        else:
            print("   ⚠️  Nenhum artista encontrado. Execute 'python init_artists.py' primeiro.")
            return
        
        # 3. Testar relacionamentos com joinedload
        print("3. Testando relacionamentos com joinedload...")
        
        # Testar get_by_id com relacionamentos
        if artists:
            artist_with_relations = artist_repo.get_by_id(artists[0].id, include_relations=True)
            if artist_with_relations:
                print(f"   ✅ Artist com relacionamentos carregado: ID {artist_with_relations.id}")
                print(f"      - Profile ID: {artist_with_relations.profile_id}")
                print(f"      - Artist Type ID: {artist_with_relations.artist_type_id}")
            else:
                print("   ❌ Falha ao carregar artist com relacionamentos")
        
        # 4. Verificar integridade referencial
        print("\n4. Verificando integridade referencial...")
        
        for artist in artists:
            # Verificar se o profile existe
            profile = profile_repo.get_by_id(artist.profile_id)
            if not profile:
                print(f"   ❌ Artist ID {artist.id}: Profile ID {artist.profile_id} não encontrado!")
            else:
                print(f"   ✅ Artist ID {artist.id}: Profile ID {artist.profile_id} existe ({profile.full_name})")
            
            # Verificar se o artist_type existe
            artist_type = artist_type_repo.get_by_id(artist.artist_type_id)
            if not artist_type:
                print(f"   ❌ Artist ID {artist.id}: Artist Type ID {artist.artist_type_id} não encontrado!")
            else:
                print(f"   ✅ Artist ID {artist.id}: Artist Type ID {artist.artist_type_id} existe ({artist_type.tipo})")
        
        print("\n🎉 Teste de relacionamentos concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    test_relationships() 