import pytest
from fastapi.testclient import TestClient

def get_auth_token(client: TestClient):
    """Helper para obter token de autenticação"""
    # Criar usuário
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass"
    }
    client.post("/api/v1/users/", json=user_data)
    
    # Fazer login
    login_data = {
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token_data = response.json()
    return f"Bearer {token_data['access_token']}"

def test_create_artist(client: TestClient):
    """Teste para criar um artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    artist_data = {
        "profile_id": 1,  # Profile com role ARTISTA (já tem artista)
        "artist_type_id": 1,
        "dias_apresentacao": ["sexta", "sábado"],
        "raio_atuacao": 50.0,
        "duracao_apresentacao": 2.0,
        "valor_hora": 100.0,
        "valor_couvert": 20.0,
        "requisitos_minimos": "Sistema de som básico"
    }

    response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
    # Espera-se erro pois já existe um artista para este profile
    assert response.status_code == 400
    assert "Já existe um artista cadastrado para este profile" in response.json()["detail"]

def test_get_artists(client: TestClient):
    """Teste para listar artistas"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    response = client.get("/api/v1/artists/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_by_id(client: TestClient):
    """Teste para obter artista por ID"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1

    response = client.get(f"/api/v1/artists/{artist_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_id
    assert "profile_id" in data
    assert "artist_type_id" in data

def test_update_artist(client: TestClient):
    """Teste para atualizar artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1

    # Atualizar o artista
    update_data = {
        "valor_hora": 150.0,
        "valor_couvert": 25.0,
        "requisitos_minimos": "Sistema de som profissional"
    }

    response = client.put(f"/api/v1/artists/{artist_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["valor_hora"] == update_data["valor_hora"]
    assert data["valor_couvert"] == update_data["valor_couvert"]
    assert data["requisitos_minimos"] == update_data["requisitos_minimos"]

def test_delete_artist(client: TestClient):
    """Teste para deletar artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1

    # Deletar o artista
    response = client.delete(f"/api/v1/artists/{artist_id}", headers=headers)
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o artista foi deletado
    get_response = client.get(f"/api/v1/artists/{artist_id}", headers=headers)
    assert get_response.status_code == 404 