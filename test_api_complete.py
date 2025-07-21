#!/usr/bin/env python3
"""
Script completo para testar a API com autenticação e relacionamentos
"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_complete():
    """Testar a API completa com autenticação"""
    print("🔍 Testando API completa com relacionamentos...")
    
    base_url = "http://localhost:8000/api/v1"
    
    try:
        # 1. Fazer login para obter token
        print("\n1. Fazendo login...")
        login_data = {
            "email": "test@eshow.com",
            "password": "test123"
        }
        
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login realizado com sucesso")
            print(f"      - Token obtido: {access_token[:20]}...")
        else:
            print(f"   ❌ Falha no login: {response.status_code}")
            print(f"      - Resposta: {response.text}")
            return
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 2. Testar GET artist sem relacionamentos
        print("\n2. Testando GET artist sem relacionamentos...")
        response = requests.get(f"{base_url}/artists/1", headers=headers)
        if response.status_code == 200:
            artist = response.json()
            print(f"   ✅ Artist obtido com sucesso")
            print(f"      - ID: {artist.get('id')}")
            print(f"      - Profile ID: {artist.get('profile_id')}")
            print(f"      - Artist Type ID: {artist.get('artist_type_id')}")
            print(f"      - Profile nos dados: {'profile' in artist}")
            print(f"      - Artist Type nos dados: {'artist_type' in artist}")
        else:
            print(f"   ❌ Falha ao obter artist: {response.status_code}")
            print(f"      - Resposta: {response.text}")
        
        # 3. Testar GET artist com relacionamentos
        print("\n3. Testando GET artist com relacionamentos...")
        response = requests.get(f"{base_url}/artists/1?include_relations=true", headers=headers)
        if response.status_code == 200:
            artist = response.json()
            print(f"   ✅ Artist com relacionamentos obtido com sucesso")
            print(f"      - ID: {artist.get('id')}")
            print(f"      - Profile ID: {artist.get('profile_id')}")
            print(f"      - Artist Type ID: {artist.get('artist_type_id')}")
            print(f"      - Profile nos dados: {'profile' in artist}")
            print(f"      - Artist Type nos dados: {'artist_type' in artist}")
            
            if 'profile' in artist and artist['profile']:
                print(f"      - Profile: {artist['profile'].get('full_name')}")
            else:
                print(f"      - ❌ Profile não foi incluído")
            
            if 'artist_type' in artist and artist['artist_type']:
                print(f"      - Artist Type: {artist['artist_type'].get('tipo')}")
            else:
                print(f"      - ❌ Artist Type não foi incluído")
        else:
            print(f"   ❌ Falha ao obter artist com relacionamentos: {response.status_code}")
            print(f"      - Resposta: {response.text}")
        
        # 4. Testar GET artists (lista) sem relacionamentos
        print("\n4. Testando GET artists (lista) sem relacionamentos...")
        response = requests.get(f"{base_url}/artists/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Artists obtidos com sucesso")
            print(f"      - Tipo de resposta: {type(data).__name__}")
            if isinstance(data, dict) and 'items' in data:
                artists = data['items']
                print(f"      - Número de artists: {len(artists)}")
                if artists:
                    artist = artists[0]
                    print(f"      - Primeiro artist ID: {artist.get('id')}")
                    print(f"      - Profile nos dados: {'profile' in artist}")
                    print(f"      - Artist Type nos dados: {'artist_type' in artist}")
            else:
                print(f"      - Resposta inesperada: {type(data)}")
        else:
            print(f"   ❌ Falha ao obter artists: {response.status_code}")
            print(f"      - Resposta: {response.text}")
        
        # 5. Testar GET artists (lista) com relacionamentos
        print("\n5. Testando GET artists (lista) com relacionamentos...")
        response = requests.get(f"{base_url}/artists/?include_relations=true", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Artists com relacionamentos obtidos com sucesso")
            print(f"      - Tipo de resposta: {type(data).__name__}")
            if isinstance(data, dict) and 'items' in data:
                artists = data['items']
                print(f"      - Número de artists: {len(artists)}")
                if artists:
                    artist = artists[0]
                    print(f"      - Primeiro artist ID: {artist.get('id')}")
                    print(f"      - Profile nos dados: {'profile' in artist}")
                    print(f"      - Artist Type nos dados: {'artist_type' in artist}")
                    
                    if 'profile' in artist and artist['profile']:
                        print(f"      - Profile: {artist['profile'].get('full_name')}")
                    else:
                        print(f"      - ❌ Profile não foi incluído")
                    
                    if 'artist_type' in artist and artist['artist_type']:
                        print(f"      - Artist Type: {artist['artist_type'].get('tipo')}")
                    else:
                        print(f"      - ❌ Artist Type não foi incluído")
            else:
                print(f"      - Resposta inesperada: {type(data)}")
        else:
            print(f"   ❌ Falha ao obter artists com relacionamentos: {response.status_code}")
            print(f"      - Resposta: {response.text}")
        
        print("\n🎉 Teste da API completa concluído!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_complete() 