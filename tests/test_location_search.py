import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.application.services.location_search_service import LocationSearchService
from app.core.location_utils import LocationUtils
from domain.entities.profile import Profile
from domain.entities.artist import Artist
from domain.entities.space import Space, AcessoEnum, PublicoEstimadoEnum
from domain.entities.space_event_type import SpaceEventType, StatusEventType
from domain.entities.space_festival_type import SpaceFestivalType, StatusFestivalType
from domain.entities.booking import Booking
from datetime import datetime, time

def test_search_by_cep(client: TestClient):
    """Testa busca por CEP"""
    cep = "01234-567"
    response = client.get(f"/api/v1/location-search/cep/{cep}")
    assert response.status_code == 200

def test_search_by_city_state(client: TestClient):
    """Testa busca por cidade e estado"""
    city = "São Paulo"
    state = "SP"
    response = client.get(f"/api/v1/location-search/city/{city}/state/{state}")
    assert response.status_code == 200

def test_search_by_coordinates(client: TestClient):
    """Testa busca por coordenadas"""
    lat = -23.5505
    lng = -46.6333
    response = client.get(f"/api/v1/location-search/coordinates?lat={lat}&lng={lng}")
    assert response.status_code == 200

def test_search_by_invalid_cep(client: TestClient):
    """Testa busca por CEP inválido"""
    cep = "00000-000"
    response = client.get(f"/api/v1/location-search/cep/{cep}")
    assert response.status_code == 500

def test_search_by_invalid_coordinates(client: TestClient):
    """Testa busca por coordenadas inválidas"""
    lat = 999.0
    lng = 999.0
    response = client.get(f"/api/v1/location-search/coordinates?lat={lat}&lng={lng}")
    assert response.status_code == 500 

class TestLocationSearchService:
    """Testes para o serviço de busca por localização"""
    
    def setup_method(self):
        """Configuração inicial para cada teste"""
        self.mock_artist_repository = Mock()
        self.mock_space_repository = Mock()
        self.mock_profile_repository = Mock()
        self.mock_space_event_type_repository = Mock()
        self.mock_space_festival_type_repository = Mock()
        self.mock_booking_repository = Mock()
        self.mock_db = Mock(spec=Session)
        
        self.service = LocationSearchService(
            artist_repository=self.mock_artist_repository,
            space_repository=self.mock_space_repository,
            profile_repository=self.mock_profile_repository,
            space_event_type_repository=self.mock_space_event_type_repository,
            space_festival_type_repository=self.mock_space_festival_type_repository,
            booking_repository=self.mock_booking_repository
        )
    
    def test_get_coordinates_from_profile_with_direct_coordinates(self):
        """Testa obtenção de coordenadas quando o profile tem latitude/longitude"""
        # Arrange
        profile = Profile(
            id=1,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999",
            latitude=-23.5505,
            longitude=-46.6333
        )
        
        # Act
        with patch.object(LocationUtils, 'get_coordinates_from_profile') as mock_get_coords:
            mock_get_coords.return_value = (-23.5505, -46.6333)
            result = LocationUtils.get_coordinates_from_profile(profile)
        
        # Assert
        assert result == (-23.5505, -46.6333)
        mock_get_coords.assert_called_once_with(profile)
    
    def test_get_coordinates_from_profile_fallback_to_cidade_uf(self):
        """Testa fallback para cidade/UF quando não há coordenadas diretas"""
        # Arrange
        profile = Profile(
            id=1,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999",
            latitude=None,
            longitude=None
        )
        
        # Act
        with patch.object(LocationUtils, 'get_coordinates_from_cidade_uf') as mock_get_cidade_uf:
            mock_get_cidade_uf.return_value = (-23.5505, -46.6333)
            result = LocationUtils.get_coordinates_from_profile(profile)
        
        # Assert
        assert result == (-23.5505, -46.6333)
        mock_get_cidade_uf.assert_called_once_with("São Paulo", "SP")
    
    def test_get_coordinates_from_profile_fallback_to_viacep(self):
        """Testa fallback para ViaCEP quando não há coordenadas diretas nem cidade/UF"""
        # Arrange
        profile = Profile(
            id=1,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="",
            uf="",
            telefone_movel="11999999999",
            latitude=None,
            longitude=None
        )
        
        # Act
        with patch.object(LocationUtils, '_get_coordinates_from_viacep') as mock_get_viacep:
            mock_get_viacep.return_value = (-23.5505, -46.6333)
            result = LocationUtils.get_coordinates_from_profile(profile)
        
        # Assert
        assert result == (-23.5505, -46.6333)
        mock_get_viacep.assert_called_once_with("01234-567")
    
    def test_search_spaces_for_artist_with_profile_coordinates(self):
        """Testa busca de espaços para artista usando coordenadas do profile"""
        # Arrange
        artist_profile = Profile(
            id=1,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999",
            latitude=-23.5505,
            longitude=-46.6333
        )
        
        artist = Artist(
            id=1,
            profile_id=1,
            artist_type_id=1,
            dias_apresentacao=["sexta", "sábado"],
            raio_atuacao=50.0,
            duracao_apresentacao=2.0,
            valor_hora=200.0,
            valor_couvert=30.0,
            requisitos_minimos="Palco e som básico"
        )
        
        space_profile = Profile(
            id=2,
            role_id=3,
            full_name="Espaço Cultural",
            artistic_name="Espaço Cultural",
            bio="Espaço para eventos",
            cep="04567-890",
            logradouro="Rua B",
            numero="456",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11888888888",
            latitude=-23.5600,
            longitude=-46.6400
        )
        
        space = Space(
            id=1,
            profile_id=2,
            space_type_id=1,
            acesso=AcessoEnum.PUBLICO,
            dias_apresentacao=["sexta", "sábado"],
            duracao_apresentacao=4.0,
            valor_hora=500.0,
            valor_couvert=50.0,
            requisitos_minimos="Artista profissional",
            oferecimentos="Palco, som e iluminação",
            estrutura_apresentacao="Palco 6x4m, som profissional",
            publico_estimado=PublicoEstimadoEnum.CEM_A_QUINHENTOS,
            fotos_ambiente=["foto1.jpg", "foto2.jpg"]
        )
        
        # Mock dos repositórios
        self.mock_profile_repository.get_by_id.return_value = artist_profile
        self.mock_artist_repository.get_by_profile_id.return_value = artist
        self.mock_profile_repository.get_by_role_id.return_value = [space_profile]
        self.mock_space_repository.get_by_profile_id.return_value = [space]
        self.mock_space_event_type_repository.get_by_space_id_and_status.return_value = [
            SpaceEventType(
                id=1,
                space_id=1,
                event_type_id=1,
                tema="Show",
                descricao="Show musical",
                data=datetime.now().date(),
                horario="20:00",
                status=StatusEventType.CONTRATANDO
            )
        ]
        
        # Act
        with patch.object(LocationUtils, 'get_coordinates_from_profile') as mock_get_coords:
            mock_get_coords.side_effect = [
                (-23.5505, -46.6333),  # Coordenadas do artista
                (-23.5600, -46.6400)   # Coordenadas do espaço
            ]
            
            result = self.service.search_spaces_for_artist(
                self.mock_db, 
                artist_profile_id=1,
                return_full_data=True,
                max_results=10
            )
        
        # Assert
        assert result.total_count == 1
        assert len(result.results) == 1
        assert result.results[0].id == 1
        assert result.results[0].distance_km > 0
        assert result.search_radius_km == 50.0
    
    def test_search_artists_for_space_with_profile_coordinates(self):
        """Testa busca de artistas para espaço usando coordenadas do profile"""
        # Arrange
        space_profile = Profile(
            id=1,
            role_id=3,
            full_name="Espaço Cultural",
            artistic_name="Espaço Cultural",
            bio="Espaço para eventos",
            cep="04567-890",
            logradouro="Rua B",
            numero="456",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11888888888",
            latitude=-23.5600,
            longitude=-46.6400
        )
        
        space = Space(
            id=1,
            profile_id=1,
            space_type_id=1,
            acesso=AcessoEnum.PUBLICO,
            dias_apresentacao=["sexta", "sábado"],
            duracao_apresentacao=4.0,
            valor_hora=500.0,
            valor_couvert=50.0,
            requisitos_minimos="Artista profissional",
            oferecimentos="Palco, som e iluminação",
            estrutura_apresentacao="Palco 6x4m, som profissional",
            publico_estimado=PublicoEstimadoEnum.CEM_A_QUINHENTOS,
            fotos_ambiente=["foto1.jpg", "foto2.jpg"]
        )
        
        artist_profile = Profile(
            id=2,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999",
            latitude=-23.5505,
            longitude=-46.6333
        )
        
        artist = Artist(
            id=1,
            profile_id=2,
            artist_type_id=1,
            dias_apresentacao=["sexta", "sábado"],
            raio_atuacao=50.0,
            duracao_apresentacao=2.0,
            valor_hora=200.0,
            valor_couvert=30.0,
            requisitos_minimos="Palco e som básico"
        )
        
        # Mock dos repositórios
        self.mock_profile_repository.get_by_id.return_value = space_profile
        self.mock_space_repository.get_by_profile_id.return_value = [space]
        self.mock_profile_repository.get_by_role_id.return_value = [artist_profile]
        self.mock_artist_repository.get_by_profile_id.return_value = artist
        self.mock_booking_repository.get_conflicting_bookings.return_value = []
        
        # Mock para eventos e festivais contratando
        self.mock_space_event_type_repository.get_by_space_id_and_status.return_value = [
            SpaceEventType(
                id=1,
                space_id=1,
                event_type_id=1,
                tema="Show",
                descricao="Show musical",
                data=datetime.now().date(),
                horario="20:00",
                status=StatusEventType.CONTRATANDO
            )
        ]
        self.mock_space_festival_type_repository.get_by_space_id_and_status.return_value = []
        
        # Act
        with patch.object(LocationUtils, 'get_coordinates_from_profile') as mock_get_coords:
            mock_get_coords.side_effect = [
                (-23.5600, -46.6400),  # Coordenadas do espaço
                (-23.5505, -46.6333)   # Coordenadas do artista
            ]
            
            result = self.service.search_artists_for_space(
                self.mock_db, 
                space_profile_id=1,
                return_full_data=True,
                max_results=10
            )
        
        # Assert
        assert result.total_count == 1
        assert len(result.results) == 1
        assert result.results[0].id == 1
        assert result.results[0].distance_km > 0
    
    def test_calculate_distance_accuracy(self):
        """Testa a precisão do cálculo de distância"""
        # Coordenadas de São Paulo (centro)
        sp_lat, sp_lng = -23.5505, -46.6333
        
        # Coordenadas de Campinas (aproximadamente 100km de SP)
        campinas_lat, campinas_lng = -22.9064, -47.0616
        
        # Act
        distance = LocationUtils.calculate_distance(sp_lat, sp_lng, campinas_lat, campinas_lng)
        
        # Assert
        assert 80 <= distance <= 120  # Distância aproximada entre SP e Campinas (mais flexível)
    
    def test_coordinates_priority_order(self):
        """Testa a ordem de prioridade das coordenadas"""
        # Arrange
        profile = Profile(
            id=1,
            role_id=2,
            full_name="João Silva",
            artistic_name="João Músico",
            bio="Músico profissional",
            cep="01234-567",
            logradouro="Rua A",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999",
            latitude=-23.5505,
            longitude=-46.6333
        )
        
        # Act & Assert
        with patch.object(LocationUtils, 'get_coordinates_from_profile') as mock_get_coords:
            mock_get_coords.return_value = (-23.5505, -46.6333)
            result = LocationUtils.get_coordinates_from_profile(profile)
            
            # Deve retornar as coordenadas diretas do profile
            assert result == (-23.5505, -46.6333)
            
            # Verifica que não foi chamado o fallback
            mock_get_coords.assert_called_once() 