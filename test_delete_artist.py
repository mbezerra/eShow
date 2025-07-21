#!/usr/bin/env python3
"""
Teste específico para o endpoint DELETE de artists
"""
import requests
import json

# Configurações
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
ARTISTS_URL = f"{BASE_URL}/api/v1/artists"

def test_delete_artist():
    """Testar o endpoint DELETE de artists"""
    print("🧪 Testando endpoint DELETE de artists...")
    
    # 1. Fazer login para obter token
    print("\n1. Fazendo login...")
    login_data = {
        "email": "test@eshow.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"   ✅ Login realizado com sucesso")
        print(f"   - Token obtido: {access_token[:20]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro no login: {e}")
        return False
    
    # Headers para requisições autenticadas
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Criar um artista para testar o DELETE
    print("\n2. Criando artista para teste...")
    artist_data = {
        "profile_id": 1,
        "artist_type_id": 1,
        "dias_apresentacao": ["sexta", "sábado"],
        "raio_atuacao": 30.0,
        "duracao_apresentacao": 1.5,
        "valor_hora": 120.0,
        "valor_couvert": 15.0,
        "requisitos_minimos": "Sistema de som básico",
        "instagram": "https://instagram.com/test_artist"
    }
    
    try:
        response = requests.post(ARTISTS_URL, json=artist_data, headers=headers)
        response.raise_for_status()
        
        created_artist = response.json()
        artist_id = created_artist["id"]
        print(f"   ✅ Artista criado com sucesso")
        print(f"   - ID: {artist_id}")
        print(f"   - Profile ID: {created_artist['profile_id']}")
        print(f"   - Artist Type ID: {created_artist['artist_type_id']}")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro ao criar artista: {e}")
        return False
    
    # 3. Testar DELETE do artista
    print(f"\n3. Testando DELETE do artista {artist_id}...")
    
    try:
        response = requests.delete(f"{ARTISTS_URL}/{artist_id}", headers=headers)
        response.raise_for_status()
        
        # Verificar status code
        print(f"   ✅ DELETE realizado com sucesso")
        print(f"   - Status Code: {response.status_code}")
        
        # Verificar se retornou mensagem
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"   - Resposta: {response_data}")
                
                if "message" in response_data:
                    print(f"   ✅ Mensagem de sucesso retornada: {response_data['message']}")
                else:
                    print(f"   ⚠️ Resposta não contém campo 'message'")
                    
            except json.JSONDecodeError:
                print(f"   ⚠️ Resposta não é JSON válido")
                print(f"   - Conteúdo: {response.text}")
        else:
            print(f"   ⚠️ Status code inesperado: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro no DELETE: {e}")
        return False
    
    # 4. Verificar se o artista foi realmente deletado
    print(f"\n4. Verificando se artista foi deletado...")
    
    try:
        response = requests.get(f"{ARTISTS_URL}/{artist_id}", headers=headers)
        
        if response.status_code == 404:
            print(f"   ✅ Artista não encontrado (deletado com sucesso)")
        else:
            print(f"   ⚠️ Artista ainda existe (status: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro ao verificar: {e}")
    
    print("\n🎉 Teste do DELETE concluído!")
    return True

if __name__ == "__main__":
    test_delete_artist() 