import pytest
from fastapi.testclient import TestClient

def test_search_by_cep(client: TestClient):
    """Teste para buscar localização por CEP"""
    cep = "01234-567"
    
    response = client.get(f"/api/v1/location-search/cep/{cep}")
    assert response.status_code == 200
    
    data = response.json()
    assert "cep" in data
    assert "city" in data
    assert "state" in data

def test_search_by_city_state(client: TestClient):
    """Teste para buscar localização por cidade e estado"""
    city = "São Paulo"
    state = "SP"
    
    response = client.get(f"/api/v1/location-search/city/{city}/state/{state}")
    assert response.status_code == 200
    
    data = response.json()
    assert "city" in data
    assert "state" in data

def test_search_by_coordinates(client: TestClient):
    """Teste para buscar localização por coordenadas"""
    lat = -23.5505
    lng = -46.6333
    
    response = client.get(f"/api/v1/location-search/coordinates?lat={lat}&lng={lng}")
    assert response.status_code == 200
    
    data = response.json()
    assert "city" in data
    assert "state" in data

def test_search_invalid_cep(client: TestClient):
    """Teste para buscar CEP inválido"""
    cep = "00000-000"
    
    response = client.get(f"/api/v1/location-search/cep/{cep}")
    assert response.status_code == 500

def test_search_invalid_coordinates(client: TestClient):
    """Teste para buscar coordenadas inválidas"""
    lat = 999.0
    lng = 999.0
    
    response = client.get(f"/api/v1/location-search/coordinates?lat={lat}&lng={lng}")
    assert response.status_code == 500 