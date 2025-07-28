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

def test_create_artist_type(client: TestClient):
    """Teste para criar um tipo de artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    artist_type_data = {
        "tipo": "Dupla"
    }
    
    response = client.post("/api/v1/artist-types/", json=artist_type_data, headers=headers)
    print(f"Create artist type response: {response.status_code} - {response.json()}")  # Debug
    assert response.status_code == 201
    
    data = response.json()
    assert data["tipo"] == artist_type_data["tipo"]
    assert "id" in data

def test_get_artist_types(client: TestClient):
    """Teste para listar tipos de artistas"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    response = client.get("/api/v1/artist-types/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_artist_type_by_id(client: TestClient):
    """Teste para obter tipo de artista por ID"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Usar um tipo existente (ID 1 deve existir após a inicialização)
    artist_type_id = 1
    
    # Buscar o tipo
    response = client.get(f"/api/v1/artist-types/{artist_type_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_type_id
    assert "tipo" in data

def test_update_artist_type(client: TestClient):
    """Teste para atualizar tipo de artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Usar um tipo existente (ID 1 deve existir após a inicialização)
    artist_type_id = 1
    
    # Atualizar o tipo
    update_data = {
        "tipo": "Trio"
    }
    
    response = client.put(f"/api/v1/artist-types/{artist_type_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["tipo"] == update_data["tipo"]

def test_delete_artist_type(client: TestClient):
    """Teste para deletar tipo de artista"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um tipo de artista temporário
    artist_type_data = {
        "tipo": "Banda"
    }
    
    create_response = client.post("/api/v1/artist-types/", json=artist_type_data, headers=headers)
    artist_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/artist-types/{artist_type_id}", headers=headers)
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/artist-types/{artist_type_id}", headers=headers)
    assert get_response.status_code == 404 