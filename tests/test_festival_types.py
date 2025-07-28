import pytest
from fastapi.testclient import TestClient

def test_create_festival_type(client: TestClient, db_session):
    """Teste para criar um tipo de festival"""
    festival_type_data = {
        "type": "Jazz Festival"
    }
    
    response = client.post("/api/v1/festival-types/", json=festival_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["type"] == festival_type_data["type"]
    assert "id" in data

def test_get_festival_types(client: TestClient, db_session):
    """Teste para listar tipos de festivais"""
    response = client.get("/api/v1/festival-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_festival_type_by_id(client: TestClient, db_session):
    """Teste para obter tipo de festival por ID"""
    # Primeiro criar um tipo de festival
    festival_type_data = {
        "type": "Rock Festival"
    }
    
    create_response = client.post("/api/v1/festival-types/", json=festival_type_data)
    festival_type_id = create_response.json()["id"]
    
    # Agora buscar o tipo criado
    response = client.get(f"/api/v1/festival-types/{festival_type_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == festival_type_id
    assert data["type"] == festival_type_data["type"]

def test_update_festival_type(client: TestClient, db_session):
    """Teste para atualizar tipo de festival"""
    # Primeiro criar um tipo de festival
    festival_type_data = {
        "type": "Blues Festival"
    }
    
    create_response = client.post("/api/v1/festival-types/", json=festival_type_data)
    festival_type_id = create_response.json()["id"]
    
    # Atualizar o tipo
    update_data = {
        "type": "Blues & Jazz Festival"
    }
    
    response = client.put(f"/api/v1/festival-types/{festival_type_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["type"] == update_data["type"]

def test_delete_festival_type(client: TestClient, db_session):
    """Teste para deletar tipo de festival"""
    # Primeiro criar um tipo de festival
    festival_type_data = {
        "type": "Temporário"
    }
    
    create_response = client.post("/api/v1/festival-types/", json=festival_type_data)
    festival_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/festival-types/{festival_type_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/festival-types/{festival_type_id}")
    assert get_response.status_code == 404 