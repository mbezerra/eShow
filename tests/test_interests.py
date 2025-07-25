import pytest
from fastapi.testclient import TestClient

def test_create_interest(client: TestClient):
    """Teste para criar um interesse"""
    interest_data = {
        "name": "Jazz",
        "description": "Interesse em música jazz",
        "category": "music"
    }
    
    response = client.post("/api/v1/interests/", json=interest_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == interest_data["name"]
    assert data["description"] == interest_data["description"]
    assert data["category"] == interest_data["category"]
    assert "id" in data

def test_get_interests(client: TestClient):
    """Teste para listar interesses"""
    response = client.get("/api/v1/interests/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_interest_by_id(client: TestClient):
    """Teste para obter interesse por ID"""
    # Primeiro criar um interesse
    interest_data = {
        "name": "Rock",
        "description": "Interesse em música rock",
        "category": "music"
    }
    
    create_response = client.post("/api/v1/interests/", json=interest_data)
    interest_id = create_response.json()["id"]
    
    # Agora buscar o interesse criado
    response = client.get(f"/api/v1/interests/{interest_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == interest_id
    assert data["name"] == interest_data["name"]

def test_update_interest(client: TestClient):
    """Teste para atualizar interesse"""
    # Primeiro criar um interesse
    interest_data = {
        "name": "Blues",
        "description": "Interesse em blues",
        "category": "music"
    }
    
    create_response = client.post("/api/v1/interests/", json=interest_data)
    interest_id = create_response.json()["id"]
    
    # Atualizar o interesse
    update_data = {
        "name": "Blues Clássico",
        "description": "Interesse em blues clássico"
    }
    
    response = client.put(f"/api/v1/interests/{interest_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

def test_delete_interest(client: TestClient):
    """Teste para deletar interesse"""
    # Primeiro criar um interesse
    interest_data = {
        "name": "Temporário",
        "description": "Interesse temporário",
        "category": "other"
    }
    
    create_response = client.post("/api/v1/interests/", json=interest_data)
    interest_id = create_response.json()["id"]
    
    # Deletar o interesse
    response = client.delete(f"/api/v1/interests/{interest_id}")
    assert response.status_code == 204
    
    # Verificar se o interesse foi deletado
    get_response = client.get(f"/api/v1/interests/{interest_id}")
    assert get_response.status_code == 404

def test_get_interests_by_category(client: TestClient):
    """Teste para obter interesses por categoria"""
    # Primeiro criar um interesse
    interest_data = {
        "name": "MPB",
        "description": "Interesse em MPB",
        "category": "music"
    }
    
    client.post("/api/v1/interests/", json=interest_data)
    
    # Buscar interesses por categoria
    response = client.get("/api/v1/interests/category/music")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list) 