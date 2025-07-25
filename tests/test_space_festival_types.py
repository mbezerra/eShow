import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_space_festival_type(client: TestClient):
    """Teste para criar uma associação espaço-tipo de festival"""
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1,
        "tema": "Festival de Jazz",
        "descricao": "Um festival incrível de jazz com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-01T19:00:00",
        "horario": "19:00"
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
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_space_festival_type_by_id(client: TestClient):
    """Teste para obter associação espaço-tipo de festival por ID"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1,
        "tema": "Festival de Rock",
        "descricao": "Um festival incrível de rock com bandas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-02T20:00:00",
        "horario": "20:00"
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
        "festival_type_id": 1,
        "tema": "Festival de Blues",
        "descricao": "Um festival incrível de blues com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-03T21:00:00",
        "horario": "21:00"
    }
    
    client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    
    # Buscar tipos de festivais do espaço
    response = client.get("/api/v1/space-festival-types/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_space_festival_types_by_festival_type(client: TestClient):
    """Teste para obter espaços de um tipo de festival específico"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1,
        "tema": "Festival de Samba",
        "descricao": "Um festival incrível de samba com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-04T22:00:00",
        "horario": "22:00"
    }
    
    client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    
    # Buscar espaços do tipo de festival
    response = client.get("/api/v1/space-festival-types/festival-type/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_delete_space_festival_type(client: TestClient):
    """Teste para deletar associação espaço-tipo de festival"""
    # Primeiro criar uma associação
    space_festival_type_data = {
        "space_id": 1,
        "festival_type_id": 1,
        "tema": "Festival de MPB",
        "descricao": "Um festival incrível de MPB com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-05T23:00:00",
        "horario": "23:00"
    }
    
    create_response = client.post("/api/v1/space-festival-types/", json=space_festival_type_data)
    association_id = create_response.json()["id"]
    
    # Deletar a associação
    response = client.delete(f"/api/v1/space-festival-types/{association_id}")
    assert response.status_code == 200
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/space-festival-types/{association_id}")
    assert get_response.status_code == 404 