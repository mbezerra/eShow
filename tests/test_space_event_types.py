import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_space_event_type(client: TestClient):
    """Teste para criar uma associação espaço-tipo de evento"""
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1,
        "tema": "Show de Jazz",
        "descricao": "Uma apresentação incrível de jazz com músicos locais",
        "status": "CONTRATANDO",
        "data": "2025-08-01T19:00:00",
        "horario": "19:00"
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
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_space_event_type_by_id(client: TestClient):
    """Teste para obter associação espaço-tipo de evento por ID"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1,
        "tema": "Show de Rock",
        "descricao": "Uma apresentação incrível de rock com bandas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-02T20:00:00",
        "horario": "20:00"
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
        "event_type_id": 1,
        "tema": "Show de Blues",
        "descricao": "Uma apresentação incrível de blues com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-03T21:00:00",
        "horario": "21:00"
    }
    
    client.post("/api/v1/space-event-types/", json=space_event_type_data)
    
    # Buscar tipos de eventos do espaço
    response = client.get("/api/v1/space-event-types/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_space_event_types_by_event_type(client: TestClient):
    """Teste para obter espaços de um tipo de evento específico"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1,
        "tema": "Show de Samba",
        "descricao": "Uma apresentação incrível de samba com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-04T22:00:00",
        "horario": "22:00"
    }
    
    client.post("/api/v1/space-event-types/", json=space_event_type_data)
    
    # Buscar espaços do tipo de evento
    response = client.get("/api/v1/space-event-types/event-type/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_delete_space_event_type(client: TestClient):
    """Teste para deletar associação espaço-tipo de evento"""
    # Primeiro criar uma associação
    space_event_type_data = {
        "space_id": 1,
        "event_type_id": 1,
        "tema": "Show de MPB",
        "descricao": "Uma apresentação incrível de MPB com artistas locais",
        "status": "CONTRATANDO",
        "data": "2025-08-05T23:00:00",
        "horario": "23:00"
    }
    
    create_response = client.post("/api/v1/space-event-types/", json=space_event_type_data)
    association_id = create_response.json()["id"]
    
    # Deletar a associação
    response = client.delete(f"/api/v1/space-event-types/{association_id}")
    assert response.status_code == 200
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/space-event-types/{association_id}")
    assert get_response.status_code == 404 