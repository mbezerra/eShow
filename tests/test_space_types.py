import pytest
from fastapi.testclient import TestClient

def test_create_space_type(client: TestClient):
    """Teste para criar um tipo de espaço"""
    space_type_data = {
        "tipo": "Auditório"  # Mudando para um tipo único
    }
    
    response = client.post("/api/v1/space-types/", json=space_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["tipo"] == space_type_data["tipo"]
    assert "id" in data

def test_get_space_types(client: TestClient):
    """Teste para listar tipos de espaços"""
    response = client.get("/api/v1/space-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_type_by_id(client: TestClient):
    """Teste para obter tipo de espaço por ID"""
    # Primeiro criar um tipo de espaço
    space_type_data = {
        "tipo": "Galeria"
    }
    
    create_response = client.post("/api/v1/space-types/", json=space_type_data)
    space_type_id = create_response.json()["id"]
    
    # Agora buscar o tipo criado
    response = client.get(f"/api/v1/space-types/{space_type_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == space_type_id
    assert data["tipo"] == space_type_data["tipo"]

def test_update_space_type(client: TestClient):
    """Teste para atualizar tipo de espaço"""
    # Primeiro criar um tipo de espaço
    space_type_data = {
        "tipo": "Cinema"
    }
    
    create_response = client.post("/api/v1/space-types/", json=space_type_data)
    space_type_id = create_response.json()["id"]
    
    # Atualizar o tipo
    update_data = {
        "tipo": "Cinema Multiplex"
    }
    
    response = client.put(f"/api/v1/space-types/{space_type_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["tipo"] == update_data["tipo"]

def test_delete_space_type(client: TestClient):
    """Teste para deletar tipo de espaço"""
    # Primeiro criar um tipo de espaço
    space_type_data = {
        "tipo": "Estúdio"
    }
    
    create_response = client.post("/api/v1/space-types/", json=space_type_data)
    space_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/space-types/{space_type_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/space-types/{space_type_id}")
    assert get_response.status_code == 404 