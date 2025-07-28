import pytest
import uuid
from fastapi.testclient import TestClient

def get_auth_token(client: TestClient):
    """Helper para obter token de autenticação"""
    # Criar usuário com email único
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "name": f"Test User {unique_id}",
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    client.post("/api/v1/users/", json=user_data)
    
    # Fazer login
    login_data = {
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token_data = response.json()
    return f"Bearer {token_data['access_token']}"

def test_create_user(client: TestClient):
    """Teste para criar um usuário"""
    user_data = {
        "name": "João Silva",
        "email": "joao@example.com",
        "password": "senha123",
        "is_active": True
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["is_active"] == user_data["is_active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_users(client: TestClient):
    """Teste para listar usuários"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    response = client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_user_by_id(client: TestClient):
    """Teste para obter usuário por ID"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um usuário
    user_data = {
        "name": "Maria Santos",
        "email": "maria@example.com",
        "password": "senha456",
        "is_active": True
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Agora buscar o usuário criado
    response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

def test_update_user(client: TestClient):
    """Teste para atualizar usuário"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um usuário
    user_data = {
        "name": "Pedro Costa",
        "email": "pedro@example.com",
        "password": "senha789",
        "is_active": True
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Atualizar o usuário
    update_data = {
        "name": "Pedro Silva Costa",
        "email": "pedro.silva@example.com"
    }
    
    response = client.put(f"/api/v1/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]

def test_delete_user(client: TestClient):
    """Teste para deletar usuário"""
    # Obter token de autenticação
    auth_token = get_auth_token(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar um usuário
    user_data = {
        "name": "Ana Oliveira",
        "email": "ana@example.com",
        "password": "senha123",
        "is_active": True
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Deletar o usuário
    response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o usuário foi deletado
    get_response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert get_response.status_code == 404 