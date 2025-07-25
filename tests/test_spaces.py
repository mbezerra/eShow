import pytest
from fastapi.testclient import TestClient

def test_create_space(client: TestClient):
    """Teste para criar um espaço"""
    space_data = {
        "name": "Teatro Municipal",
        "description": "Teatro histórico da cidade",
        "address": "Rua das Artes, 123",
        "city": "São Paulo",
        "state": "SP",
        "cep": "01234-567",
        "capacity": 500,
        "space_type_id": 1,
        "is_active": True
    }
    
    response = client.post("/api/v1/spaces/", json=space_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == space_data["name"]
    assert data["description"] == space_data["description"]
    assert data["capacity"] == space_data["capacity"]
    assert "id" in data

def test_get_spaces(client: TestClient):
    """Teste para listar espaços"""
    response = client.get("/api/v1/spaces/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_by_id(client: TestClient):
    """Teste para obter espaço por ID"""
    # Primeiro criar um espaço
    space_data = {
        "name": "Auditório Central",
        "description": "Auditório para apresentações",
        "address": "Av. Principal, 456",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "cep": "20000-000",
        "capacity": 300,
        "space_type_id": 1
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Agora buscar o espaço criado
    response = client.get(f"/api/v1/spaces/{space_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == space_id
    assert data["name"] == space_data["name"]

def test_update_space(client: TestClient):
    """Teste para atualizar espaço"""
    # Primeiro criar um espaço
    space_data = {
        "name": "Galeria de Arte",
        "description": "Espaço para exposições",
        "address": "Rua das Flores, 789",
        "city": "Belo Horizonte",
        "state": "MG",
        "cep": "30000-000",
        "capacity": 100,
        "space_type_id": 1
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Atualizar o espaço
    update_data = {
        "name": "Galeria de Arte Moderna",
        "description": "Espaço para exposições de arte moderna",
        "capacity": 150
    }
    
    response = client.put(f"/api/v1/spaces/{space_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["capacity"] == update_data["capacity"]

def test_delete_space(client: TestClient):
    """Teste para deletar espaço"""
    # Primeiro criar um espaço
    space_data = {
        "name": "Espaço Temporário",
        "description": "Espaço temporário",
        "address": "Rua Temporária, 999",
        "city": "Salvador",
        "state": "BA",
        "cep": "40000-000",
        "capacity": 50,
        "space_type_id": 1
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Deletar o espaço
    response = client.delete(f"/api/v1/spaces/{space_id}")
    assert response.status_code == 204
    
    # Verificar se o espaço foi deletado
    get_response = client.get(f"/api/v1/spaces/{space_id}")
    assert get_response.status_code == 404 