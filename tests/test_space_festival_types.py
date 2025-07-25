import pytest
from fastapi.testclient import TestClient

def test_create_space_festival_type(client: TestClient):
    """Teste para criar uma associação espaço-tipo de festival"""
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1
    }
    
    response = client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["space_id"] == space_festival_type_data["space_id"]
    assert data["festival_type_id"] == space_festival_type_data["festival_type_id"]
    assert "id" in data

def test_get_space_festival_types(client: TestClient):
    """Teste para listar associações espaço-tipo de festival"""
    response = client.get("/api/v1/space-festival-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_festival_type_by_id(client: TestClient):
    """Teste para obter associação espaço-tipo de festival por ID"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1
    }
    
    create_response = client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    association_id = create_response.json()["id"]
    
    # Agora buscar a associação criada
    response = client.get(f"/api/v1/space-festival-types/{association_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == association_id
    assert data["space_id"] == space_festival_type_data["space_id"]

def test_get_space_festival_types_by_space(client: TestClient):
    """Teste para obter tipos de festivais de um espaço específico"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1
    }
    
    client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    
    # Buscar tipos de festivais do espaço
    response = client.get("/api/v1/space-festival-types/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_festival_types_by_festival_type(client: TestClient):
    """Teste para obter espaços de um tipo de festival específico"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1
    }
    
    client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    
    # Buscar espaços do tipo de festival
    response = client.get("/api/v1/space-festival-types/festival-type/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_delete_space_festival_type(client: TestClient):
    """Teste para deletar associação espaço-tipo de festival"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1
    }
    
    create_response = client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    association_id = create_response.json()["id"]
    
    # Deletar a associação
    response = client.delete(f"/api/v1/space-festival-types/{association_id}")
    assert response.status_code == 204
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/space-festival-types/{association_id}")
    assert get_response.status_code == 404 