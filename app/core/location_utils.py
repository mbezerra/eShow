import requests
import math
import unicodedata
from typing import Optional, Tuple, Dict, Any
import logging
import time
from infrastructure.database.database import SessionLocal
from infrastructure.repositories.cep_coordinates_repository_impl import CepCoordinatesRepositoryImpl

logger = logging.getLogger(__name__)

def get_location_by_cep(cep: str) -> Optional[Dict[str, Any]]:
    """Buscar localização por CEP"""
    try:
        # Simular busca por CEP (implementação básica)
        # Em produção, isso seria uma chamada para API de CEP
        if cep == "00000-000":
            return None
        
        # Retornar dados simulados para CEPs válidos
        return {
            "cep": cep,
            "city": "São Paulo",
            "state": "SP",
            "latitude": -23.5505,
            "longitude": -46.6333
        }
    except Exception as e:
        logger.error(f"Erro ao buscar localização por CEP {cep}: {str(e)}")
        return None

def get_location_by_city_state(city: str, state: str) -> Optional[Dict[str, Any]]:
    """Buscar localização por cidade e estado"""
    try:
        # Simular busca por cidade/estado
        return {
            "city": city,
            "state": state,
            "latitude": -23.5505,
            "longitude": -46.6333
        }
    except Exception as e:
        logger.error(f"Erro ao buscar localização por cidade {city}/{state}: {str(e)}")
        return None

def get_location_by_coordinates(lat: float, lng: float) -> Optional[Dict[str, Any]]:
    """Buscar localização por coordenadas"""
    try:
        # Simular busca por coordenadas
        if lat == 999.0 and lng == 999.0:
            return None
        
        return {
            "city": "São Paulo",
            "state": "SP",
            "latitude": lat,
            "longitude": lng
        }
    except Exception as e:
        logger.error(f"Erro ao buscar localização por coordenadas {lat}/{lng}: {str(e)}")
        return None

class LocationUtils:
    """Utilitário para cálculos de localização e distância"""
    
    # Cache simples para evitar requisições repetidas
    _coordinates_cache = {}
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normaliza texto removendo acentos e convertendo para maiúsculas
        
        Args:
            text: Texto a ser normalizado
            
        Returns:
            Texto normalizado sem acentos e em maiúsculas
        """
        # Remove acentos usando unicodedata
        normalized = unicodedata.normalize('NFD', text)
        # Remove caracteres de acentuação
        ascii_text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        # Converte para maiúsculas e remove espaços extras
        return ascii_text.strip().upper()
    
    @staticmethod
    def _get_cep_repository():
        """Obtém uma instância do repositório de coordenadas"""
        db = SessionLocal()
        return CepCoordinatesRepositoryImpl(db), db
    
    @staticmethod
    def get_coordinates_from_cidade_uf(cidade: str, uf: str) -> Optional[Tuple[float, float]]:
        """
        Obtém as coordenadas (latitude, longitude) de uma cidade/UF
        
        Args:
            cidade: Nome da cidade
            uf: Sigla da UF (2 caracteres)
            
        Returns:
            Tuple com (latitude, longitude) ou None se não conseguir obter
        """
        try:
            # Normalizar cidade e UF (removendo acentos)
            cidade_clean = LocationUtils._normalize_text(cidade)
            uf_clean = uf.strip().upper()
            
            # Verificar cache primeiro
            cache_key = f"{cidade_clean}_{uf_clean}"
            if cache_key in LocationUtils._coordinates_cache:
                return LocationUtils._coordinates_cache[cache_key]
            
            # Buscar na base de dados local
            coordinates = LocationUtils._get_coordinates_from_local_db(cidade_clean, uf_clean)
            
            # Armazenar no cache
            if coordinates:
                LocationUtils._coordinates_cache[cache_key] = coordinates
                logger.info(f"Coordenadas obtidas para {cidade}/{uf}: {coordinates}")
            
            return coordinates
                
        except Exception as e:
            logger.error(f"Erro ao obter coordenadas de {cidade}/{uf}: {str(e)}")
            return None
    
    @staticmethod
    def _get_coordinates_from_local_db(cidade: str, uf: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas da base de dados local"""
        try:
            repository, db = LocationUtils._get_cep_repository()
            
            try:
                # Buscar por cidade e UF (ambos normalizados)
                cep_coords = repository.get_by_cidade_uf(cidade, uf)
                
                if cep_coords:
                    logger.info(f"Coordenadas encontradas na base de dados para {cidade}/{uf}: {cep_coords.coordinates}")
                    return cep_coords.coordinates
                
                # Se não encontrar exato, tentar busca parcial por cidade
                cidades_similares = repository.search_by_cidade(cidade)
                if cidades_similares:
                    # Retornar a primeira cidade encontrada com a UF correta
                    for cidade_similar in cidades_similares:
                        if cidade_similar.uf == uf:
                            logger.info(f"Coordenadas encontradas (busca parcial) para {cidade}/{uf}: {cidade_similar.coordinates}")
                            return cidade_similar.coordinates
                
                return None
                
            finally:
                db.close()
                
        except Exception as e:
            logger.warning(f"Erro ao buscar coordenadas na base de dados para {cidade}/{uf}: {str(e)}")
            return None
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula a distância entre dois pontos usando a fórmula de Haversine
        
        Args:
            lat1, lon1: Coordenadas do primeiro ponto
            lat2, lon2: Coordenadas do segundo ponto
            
        Returns:
            Distância em quilômetros
        """
        # Raio da Terra em quilômetros
        R = 6371.0
        
        # Converter graus para radianos
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Diferenças nas coordenadas
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        # Distância em quilômetros
        distance = R * c
        
        return distance
    
    @staticmethod
    def get_nearby_cities(latitude: float, longitude: float, radius_km: float = 50) -> list:
        """
        Obtém cidades próximas a um ponto dado
        
        Args:
            latitude, longitude: Coordenadas do ponto central
            radius_km: Raio de busca em quilômetros
            
        Returns:
            Lista de cidades próximas com suas coordenadas
        """
        try:
            repository, db = LocationUtils._get_cep_repository()
            
            try:
                nearby_cities = repository.get_nearby_cities(latitude, longitude, radius_km)
                
                # Calcular distância para cada cidade
                result = []
                for city in nearby_cities:
                    distance = LocationUtils.calculate_distance(
                        latitude, longitude, 
                        city.latitude, city.longitude
                    )
                    
                    result.append({
                        'cidade': city.cidade,
                        'uf': city.uf,
                        'latitude': city.latitude,
                        'longitude': city.longitude,
                        'distancia_km': round(distance, 2)
                    })
                
                # Ordenar por distância
                result.sort(key=lambda x: x['distancia_km'])
                
                return result
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Erro ao buscar cidades próximas: {str(e)}")
            return []
    
    @staticmethod
    def search_cities_by_name(cidade: str, limit: int = 10) -> list:
        """
        Busca cidades por nome (parcial)
        
        Args:
            cidade: Nome da cidade (ou parte do nome)
            limit: Limite de resultados
            
        Returns:
            Lista de cidades encontradas
        """
        try:
            repository, db = LocationUtils._get_cep_repository()
            
            try:
                cities = repository.search_by_cidade(cidade)
                
                result = []
                for city in cities[:limit]:
                    result.append({
                        'cidade': city.cidade,
                        'uf': city.uf,
                        'latitude': city.latitude,
                        'longitude': city.longitude
                    })
                
                return result
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Erro ao buscar cidades por nome: {str(e)}")
            return [] 