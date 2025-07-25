import pytest
from fastapi.testclient import TestClient

def test_create_role(client: TestClient):
    """Teste para criar um role"""
    role_data = {
        "name": "Admin",
        "description": "Administrador do sistema"
    }
    
    response = client.post("/api/v1/roles/", json=role_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == role_data["name"]
    assert data["description"] == role_data["description"]
    assert "id" in data

def test_get_roles(client: TestClient):
    """Teste para listar roles"""
    response = client.get("/api/v1/roles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_role_by_id(client: TestClient):
    """Teste para obter role por ID"""
    # Primeiro criar um role
    role_data = {
        "name": "User",
        "description": "Usuário comum"
    }
    
    create_response = client.post("/api/v1/roles/", json=role_data)
    role_id = create_response.json()["id"]
    
    # Agora buscar o role criado
    response = client.get(f"/api/v1/roles/{role_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == role_id
    assert data["name"] == role_data["name"]

def test_update_role(client: TestClient):
    """Teste para atualizar role"""
    # Primeiro criar um role
    role_data = {
        "name": "Moderator",
        "description": "Moderador"
    }
    
    create_response = client.post("/api/v1/roles/", json=role_data)
    role_id = create_response.json()["id"]
    
    # Atualizar o role
    update_data = {
        "name": "Super Moderator",
        "description": "Super Moderador"
    }
    
    response = client.put(f"/api/v1/roles/{role_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

def test_delete_role(client: TestClient):
    """Teste para deletar role"""
    # Primeiro criar um role
    role_data = {
        "name": "Temporary",
        "description": "Role temporário"
    }
    
    create_response = client.post("/api/v1/roles/", json=role_data)
    role_id = create_response.json()["id"]
    
    # Deletar o role
    response = client.delete(f"/api/v1/roles/{role_id}")
    assert response.status_code == 204
    
    # Verificar se o role foi deletado
    get_response = client.get(f"/api/v1/roles/{role_id}")
    assert get_response.status_code == 404 