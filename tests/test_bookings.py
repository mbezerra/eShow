import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_booking(client: TestClient):
    """Teste para criar um booking"""
    tomorrow = datetime.now() + timedelta(days=1)
    day_after = datetime.now() + timedelta(days=2)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "20:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "22:00",
        "space_id": 1,  # Para agendamento de artista
        "artist_id": None
    }
    
    response = client.post("/api/v1/bookings/", json=booking_data)
    print(f"Create booking response: {response.status_code} - {response.json()}")  # Debug
    assert response.status_code == 201
    
    data = response.json()
    assert data["profile_id"] == booking_data["profile_id"]
    assert data["space_id"] == booking_data["space_id"]
    assert "id" in data

def test_get_bookings(client: TestClient):
    """Teste para listar bookings"""
    response = client.get("/api/v1/bookings/")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data  # BookingListResponse tem campo 'items'
    assert isinstance(data["items"], list)

def test_get_booking_by_id(client: TestClient):
    """Teste para obter booking por ID"""
    # Primeiro criar um booking
    tomorrow = datetime.now() + timedelta(days=3)
    day_after = datetime.now() + timedelta(days=4)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "19:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "21:00",
        "space_id": 1,
        "artist_id": None
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Agora buscar o booking criado
    response = client.get(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == booking_id
    assert data["profile_id"] == booking_data["profile_id"]

def test_update_booking(client: TestClient):
    """Teste para atualizar booking"""
    # Primeiro criar um booking
    tomorrow = datetime.now() + timedelta(days=5)
    day_after = datetime.now() + timedelta(days=6)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "18:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "20:00",
        "space_id": 1,
        "artist_id": None
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Atualizar o booking
    update_data = {
        "horario_inicio": "19:00",
        "horario_fim": "21:00"
    }
    
    response = client.put(f"/api/v1/bookings/{booking_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["horario_inicio"] == update_data["horario_inicio"]
    assert data["horario_fim"] == update_data["horario_fim"]

def test_delete_booking(client: TestClient):
    """Teste para deletar booking"""
    # Primeiro criar um booking
    tomorrow = datetime.now() + timedelta(days=7)
    day_after = datetime.now() + timedelta(days=8)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "17:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "19:00",
        "space_id": 1,
        "artist_id": None
    }
    
    create_response = client.post("/api/v1/bookings/", json=booking_data)
    booking_id = create_response.json()["id"]
    
    # Deletar o booking
    response = client.delete(f"/api/v1/bookings/{booking_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o booking foi deletado
    get_response = client.get(f"/api/v1/bookings/{booking_id}")
    assert get_response.status_code == 404

def test_get_bookings_by_space(client: TestClient):
    """Teste para obter bookings de um espaço específico"""
    # Primeiro criar um booking
    tomorrow = datetime.now() + timedelta(days=9)
    day_after = datetime.now() + timedelta(days=10)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "16:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "18:00",
        "space_id": 1,
        "artist_id": None
    }
    
    client.post("/api/v1/bookings/", json=booking_data)
    
    # Buscar bookings do espaço
    response = client.get("/api/v1/bookings/space/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data  # BookingListResponse tem campo 'items'
    assert isinstance(data["items"], list)

def test_get_bookings_by_artist(client: TestClient):
    """Teste para obter bookings de um artista específico"""
    # Primeiro criar um booking
    tomorrow = datetime.now() + timedelta(days=11)
    day_after = datetime.now() + timedelta(days=12)
    
    booking_data = {
        "profile_id": 1,  # Profile de artista
        "data_inicio": tomorrow.date().isoformat(),
        "horario_inicio": "15:00",
        "data_fim": day_after.date().isoformat(),
        "horario_fim": "17:00",
        "space_id": 1,
        "artist_id": None
    }
    
    client.post("/api/v1/bookings/", json=booking_data)
    
    # Buscar bookings do artista
    response = client.get("/api/v1/bookings/artist/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data  # BookingListResponse tem campo 'items'
    assert isinstance(data["items"], list) 