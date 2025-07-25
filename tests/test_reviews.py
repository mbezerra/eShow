import pytest
from fastapi.testclient import TestClient

def test_create_review(client: TestClient):
    """Teste para criar uma review"""
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 5,
        "comment": "Excelente apresentação!",
        "is_public": True
    }
    
    response = client.post("/api/v1/reviews/", json=review_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["booking_id"] == review_data["booking_id"]
    assert data["user_id"] == review_data["user_id"]
    assert data["rating"] == review_data["rating"]
    assert data["comment"] == review_data["comment"]
    assert "id" in data

def test_get_reviews(client: TestClient):
    """Teste para listar reviews"""
    response = client.get("/api/v1/reviews/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_review_by_id(client: TestClient):
    """Teste para obter review por ID"""
    # Primeiro criar uma review
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 4,
        "comment": "Muito bom show",
        "is_public": True
    }
    
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Agora buscar a review criada
    response = client.get(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == review_id
    assert data["booking_id"] == review_data["booking_id"]

def test_update_review(client: TestClient):
    """Teste para atualizar review"""
    # Primeiro criar uma review
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 3,
        "comment": "Show regular",
        "is_public": True
    }
    
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Atualizar a review
    update_data = {
        "rating": 4,
        "comment": "Show melhorou muito!"
    }
    
    response = client.put(f"/api/v1/reviews/{review_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["rating"] == update_data["rating"]
    assert data["comment"] == update_data["comment"]

def test_delete_review(client: TestClient):
    """Teste para deletar review"""
    # Primeiro criar uma review
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 2,
        "comment": "Review temporária",
        "is_public": False
    }
    
    create_response = client.post("/api/v1/reviews/", json=review_data)
    review_id = create_response.json()["id"]
    
    # Deletar a review
    response = client.delete(f"/api/v1/reviews/{review_id}")
    assert response.status_code == 204
    
    # Verificar se a review foi deletada
    get_response = client.get(f"/api/v1/reviews/{review_id}")
    assert get_response.status_code == 404

def test_get_reviews_by_booking(client: TestClient):
    """Teste para obter reviews de um booking específico"""
    # Primeiro criar uma review
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 5,
        "comment": "Teste por booking",
        "is_public": True
    }
    
    client.post("/api/v1/reviews/", json=review_data)
    
    # Buscar reviews do booking
    response = client.get("/api/v1/reviews/booking/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_reviews_by_user(client: TestClient):
    """Teste para obter reviews de um usuário específico"""
    # Primeiro criar uma review
    review_data = {
        "booking_id": 1,
        "user_id": 1,
        "rating": 4,
        "comment": "Teste por usuário",
        "is_public": True
    }
    
    client.post("/api/v1/reviews/", json=review_data)
    
    # Buscar reviews do usuário
    response = client.get("/api/v1/reviews/user/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list) 