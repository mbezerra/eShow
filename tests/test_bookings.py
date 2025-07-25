import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_booking(client: TestClient):
    """Teste para criar um booking"""
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=7, hours=2)).isoformat(),
        "status": "pending",
        "description": "Show de jazz"
    }
    
    response = client.post("/api/v1/bookings/", json=booking_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["space_id"] == booking_data["space_id"]
    assert data["artist_id"] == booking_data["artist_id"]
    assert data["status"] == booking_data["status"]
    assert "id" in data

def test_get_bookings(client: TestClient):
    """Teste para listar bookings"""
    response = client.get("/api/v1/bookings/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_booking_by_id(client: TestClient):
    """Teste para obter booking por ID"""
    # Primeiro criar um booking
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=14)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=14, hours=3)).isoformat(),
        "status": "confirmed",
        "description": "Workshop de música"
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Agora buscar o booking criado
    response = client.get(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == booking_id
    assert data["space_id"] == booking_data["space_id"]

def test_update_booking(client: TestClient):
    """Teste para atualizar booking"""
    # Primeiro criar um booking
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=21)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=21, hours=1)).isoformat(),
        "status": "pending",
        "description": "Apresentação inicial"
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Atualizar o booking
    update_data = {
        "status": "confirmed",
        "description": "Apresentação confirmada"
    }
    
    response = client.put(f"/api/v1/bookings/{booking_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == update_data["status"]
    assert data["description"] == update_data["description"]

def test_delete_booking(client: TestClient):
    """Teste para deletar booking"""
    # Primeiro criar um booking
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=28)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=28, hours=2)).isoformat(),
        "status": "cancelled",
        "description": "Booking cancelado"
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Deletar o booking
    response = client.delete(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 204
    
    # Verificar se o booking foi deletado
    get_response = client.get(f"/api/v1/bookings/{booking_id}")
    assert get_response.status_code == 404

def test_get_bookings_by_space(client: TestClient):
    """Teste para obter bookings de um espaço específico"""
    # Primeiro criar um booking
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=35)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=35, hours=1)).isoformat(),
        "status": "pending",
        "description": "Teste por espaço"
    }
    
    client.post("/api/v1/bookings/", json=booking_data)
    
    # Buscar bookings do espaço
    response = client.get("/api/v1/bookings/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_bookings_by_artist(client: TestClient):
    """Teste para obter bookings de um artista específico"""
    # Primeiro criar um booking
    booking_data = {
        "space_id": 1,
        "artist_id": 1,
        "start_date": (datetime.now() + timedelta(days=42)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=42, hours=2)).isoformat(),
        "status": "confirmed",
        "description": "Teste por artista"
    }
    
    client.post("/api/v1/bookings/", json=booking_data)
    
    # Buscar bookings do artista
    response = client.get("/api/v1/bookings/artist/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list) 