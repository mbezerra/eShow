import pytest
from fastapi.testclient import TestClient

def test_create_event_type(client: TestClient):
    """Teste para criar um tipo de evento"""
    event_type_data = {
        "type": "Show"
    }
    
    response = client.post("/api/v1/event-types/", json=event_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["type"] == event_type_data["type"]
    assert "id" in data

def test_get_event_types(client: TestClient):
    """Teste para listar tipos de eventos"""
    response = client.get("/api/v1/event-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_event_type_by_id(client: TestClient):
    """Teste para obter tipo de evento por ID"""
    # Primeiro criar um tipo de evento
    event_type_data = {
        "type": "Festival"
    }
    
    create_response = client.post("/api/v1/event-types/", json=event_type_data)
    event_type_id = create_response.json()["id"]
    
    # Agora buscar o tipo criado
    response = client.get(f"/api/v1/event-types/{event_type_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == event_type_id
    assert data["type"] == event_type_data["type"]

def test_update_event_type(client: TestClient):
    """Teste para atualizar tipo de evento"""
    # Primeiro criar um tipo de evento
    event_type_data = {
        "type": "Workshop"
    }
    
    create_response = client.post("/api/v1/event-types/", json=event_type_data)
    event_type_id = create_response.json()["id"]
    
    # Atualizar o tipo
    update_data = {
        "type": "Workshop de Música"
    }
    
    response = client.put(f"/api/v1/event-types/{event_type_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["type"] == update_data["type"]

def test_delete_event_type(client: TestClient):
    """Teste para deletar tipo de evento"""
    # Primeiro criar um tipo de evento
    event_type_data = {
        "type": "Temporário"
    }
    
    create_response = client.post("/api/v1/event-types/", json=event_type_data)
    event_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/event-types/{event_type_id}")
    assert response.status_code == 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/event-types/{event_type_id}")
    assert get_response.status_code == 404 