import pytest
from fastapi.testclient import TestClient

def test_create_space_event_type(client: TestClient):
    """Teste para criar uma associação espaço-tipo de evento"""
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1
    }
    
    response = client.post("/api/v1/space-event-types/", json=space_event_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["space_id"] == space_event_type_data["space_id"]
    assert data["event_type_id"] == space_event_type_data["event_type_id"]
    assert "id" in data

def test_get_space_event_types(client: TestClient):
    """Teste para listar associações espaço-tipo de evento"""
    response = client.get("/api/v1/space-event-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_event_type_by_id(client: TestClient):
    """Teste para obter associação espaço-tipo de evento por ID"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1
    }
    
    create_response = client.post("/api/v1/space-event-types/", json=space_event_type_data)
    association_id = create_response.json()["id"]
    
    # Agora buscar a associação criada
    response = client.get(f"/api/v1/space-event-types/{association_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == association_id
    assert data["space_id"] == space_event_type_data["space_id"]

def test_get_space_event_types_by_space(client: TestClient):
    """Teste para obter tipos de eventos de um espaço específico"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1
    }
    
    client.post("/api/v1/space-event-types/", json=space_event_type_data)
    
    # Buscar tipos de eventos do espaço
    response = client.get("/api/v1/space-event-types/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_event_types_by_event_type(client: TestClient):
    """Teste para obter espaços de um tipo de evento específico"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1
    }
    
    client.post("/api/v1/space-event-types/", json=space_event_type_data)
    
    # Buscar espaços do tipo de evento
    response = client.get("/api/v1/space-event-types/event-type/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_delete_space_event_type(client: TestClient):
    """Teste para deletar associação espaço-tipo de evento"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1
    }
    
    create_response = client.post("/api/v1/space-event-types/", json=space_event_type_data)
    association_id = create_response.json()["id"]
    
    # Deletar a associação
    response = client.delete(f"/api/v1/space-event-types/{association_id}")
    assert response.status_code == 204
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/space-event-types/{association_id}")
    assert get_response.status_code == 404 