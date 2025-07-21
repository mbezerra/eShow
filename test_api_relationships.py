#!/usr/bin/env python3
"""
Script para testar a API com relacionamentos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import get_database_session
from infrastructure.repositories.artist_repository_impl import ArtistRepositoryImpl

def test_api_relationships():
    """Testar se os relacionamentos estão sendo retornados corretamente"""
    print("🔍 Testando API com relacionamentos...")
    
    # Obter sessão do banco
    session = next(get_database_session())
    artist_repo = ArtistRepositoryImpl(session)
    
    try:
        # 1. Testar get_by_id sem relacionamentos
        print("\n1. Testando get_by_id sem relacionamentos...")
        artist = artist_repo.get_by_id(1, include_relations=False)
        if artist:
            print(f"   ✅ Artist encontrado: ID {artist.id}")
            print(f"      - Tipo: {type(artist).__name__}")
            print(f"      - Profile ID: {artist.profile_id}")
            print(f"      - Artist Type ID: {artist.artist_type_id}")
        else:
            print("   ❌ Artist não encontrado")
        
        # 2. Testar get_by_id com relacionamentos
        print("\n2. Testando get_by_id com relacionamentos...")
        artist_with_relations = artist_repo.get_by_id(1, include_relations=True)
        if artist_with_relations:
            print(f"   ✅ Artist com relacionamentos encontrado: ID {artist_with_relations.id}")
            print(f"      - Tipo: {type(artist_with_relations).__name__}")
            print(f"      - Profile ID: {artist_with_relations.profile_id}")
            print(f"      - Artist Type ID: {artist_with_relations.artist_type_id}")
            
            # Verificar se os relacionamentos foram carregados
            if hasattr(artist_with_relations, 'profile') and artist_with_relations.profile:
                print(f"      - Profile carregado: {artist_with_relations.profile.full_name}")
            else:
                print("      - ❌ Profile não foi carregado")
            
            if hasattr(artist_with_relations, 'artist_type') and artist_with_relations.artist_type:
                print(f"      - Artist Type carregado: {artist_with_relations.artist_type.tipo}")
            else:
                print("      - ❌ Artist Type não foi carregado")
        else:
            print("   ❌ Artist com relacionamentos não encontrado")
        
        # 3. Testar get_all com relacionamentos
        print("\n3. Testando get_all com relacionamentos...")
        artists = artist_repo.get_all(include_relations=True)
        print(f"   📊 Artists encontrados: {len(artists)}")
        
        for artist in artists:
            print(f"      - Artist ID: {artist.id}")
            print(f"        Tipo: {type(artist).__name__}")
            
            if hasattr(artist, 'profile') and artist.profile:
                print(f"        Profile: {artist.profile.full_name}")
            else:
                print(f"        Profile: Não carregado")
            
            if hasattr(artist, 'artist_type') and artist.artist_type:
                print(f"        Artist Type: {artist.artist_type.tipo}")
            else:
                print(f"        Artist Type: Não carregado")
        
        print("\n🎉 Teste de API com relacionamentos concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_api_relationships() 