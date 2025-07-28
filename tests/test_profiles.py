import pytest
import uuid
from fastapi.testclient import TestClient

def get_auth_token_and_user(client: TestClient):
    """Helper para obter token de autenticação e criar usuário"""
    # Criar usuário com email único
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "name": f"Test User {unique_id}",
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Fazer login
    login_data = {
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token_data = response.json()
    auth_token = f"Bearer {token_data['access_token']}"
    
    return auth_token, user_id

def test_create_profile(client: TestClient):
    """Teste para criar um profile"""
    # Obter token de autenticação e criar usuário
    auth_token, user_id = get_auth_token_and_user(client)
    headers = {"Authorization": auth_token}
    
    profile_data = {
        "user_id": user_id,  # Usar o usuário criado
        "role_id": 2,  # Role ARTISTA
        "full_name": "João Silva",
        "artistic_name": "João Artista",
        "bio": "Músico profissional com experiência em diversos estilos",
        "cep": "01234-567",
        "logradouro": "Rua das Flores",
        "numero": "123",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_movel": "11999999999",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    
    response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["full_name"] == profile_data["full_name"]
    assert data["artistic_name"] == profile_data["artistic_name"]
    assert data["user_id"] == profile_data["user_id"]
    assert data["latitude"] == profile_data["latitude"]
    assert data["longitude"] == profile_data["longitude"]
    assert "id" in data

def test_get_profiles(client: TestClient):
    """Teste para listar profiles"""
    # Obter token de autenticação
    auth_token, _ = get_auth_token_and_user(client)
    headers = {"Authorization": auth_token}
    
    response = client.get("/api/v1/profiles/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_profile_by_id(client: TestClient):
    """Teste para obter profile por ID"""
    # Obter token de autenticação e criar profile
    auth_token, user_id = get_auth_token_and_user(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um profile
    profile_data = {
        "user_id": user_id,
        "role_id": 2,
        "full_name": "Maria Santos",
        "artistic_name": "Maria Artista",
        "bio": "Cantora profissional",
        "cep": "04567-890",
        "logradouro": "Av. Paulista",
        "numero": "456",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_movel": "11888888888",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
    profile_id = create_response.json()["id"]
    
    # Buscar o profile criado
    response = client.get(f"/api/v1/profiles/{profile_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == profile_id
    assert "bio" in data
    assert "full_name" in data
    # Verificar se os campos de latitude e longitude estão presentes (mesmo que sejam None)
    assert "latitude" in data
    assert "longitude" in data

def test_update_profile(client: TestClient):
    """Teste para atualizar profile"""
    # Obter token de autenticação e criar profile
    auth_token, user_id = get_auth_token_and_user(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um profile
    profile_data = {
        "user_id": user_id,
        "role_id": 2,
        "full_name": "Pedro Costa",
        "artistic_name": "Pedro Artista",
        "bio": "Músico iniciante",
        "cep": "07890-123",
        "logradouro": "Rua Augusta",
        "numero": "789",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_movel": "11777777777",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
    profile_id = create_response.json()["id"]
    
    # Atualizar o profile
    update_data = {
        "bio": "Músico profissional com experiência em diversos estilos",
        "telefone_movel": "11666666666",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    
    response = client.put(f"/api/v1/profiles/{profile_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["bio"] == update_data["bio"]
    assert data["telefone_movel"] == update_data["telefone_movel"]
    assert data["latitude"] == update_data["latitude"]
    assert data["longitude"] == update_data["longitude"]

def test_delete_profile(client: TestClient):
    """Teste para deletar profile"""
    # Obter token de autenticação e criar profile
    auth_token, user_id = get_auth_token_and_user(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um profile
    profile_data = {
        "user_id": user_id,
        "role_id": 2,
        "full_name": "Ana Oliveira",
        "artistic_name": "Ana Artista",
        "bio": "Cantora profissional",
        "cep": "01234-567",
        "logradouro": "Rua das Flores",
        "numero": "123",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_movel": "11555555555",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
    profile_id = create_response.json()["id"]

    # Deletar o profile
    response = client.delete(f"/api/v1/profiles/{profile_id}", headers=headers)
    assert response.status_code == 200
    
    # Verificar se o profile foi deletado
    get_response = client.get(f"/api/v1/profiles/{profile_id}", headers=headers)
    assert get_response.status_code == 404 