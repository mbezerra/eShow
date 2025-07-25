import requests
import math
from typing import Optional, Tuple
import logging
import time
from infrastructure.database.database import SessionLocal
from infrastructure.repositories.cep_coordinates_repository_impl import CepCoordinatesRepositoryImpl

logger = logging.getLogger(__name__)

class LocationUtils:
    """Utilitário para cálculos de localização e distância"""
    
    # Cache simples para evitar requisições repetidas
    _coordinates_cache = {}
    
    @staticmethod
    def _get_cep_repository():
        """Obtém uma instância do repositório de CEPs"""
        db = SessionLocal()
        return CepCoordinatesRepositoryImpl(db), db
    
    @staticmethod
    def get_coordinates_from_cep(cep: str) -> Optional[Tuple[float, float]]:
        """
        Obtém as coordenadas (latitude, longitude) de um CEP usando múltiplas fontes
        
        Args:
            cep: CEP no formato '12345-678' ou '12345678'
            
        Returns:
            Tuple com (latitude, longitude) ou None se não conseguir obter
        """
        try:
            # Normalizar CEP para formato com hífen
            cep_clean = ''.join(filter(str.isdigit, cep))
            
            if len(cep_clean) != 8:
                logger.warning(f"CEP inválido: {cep}")
                return None
            
            # Formatar CEP com hífen para busca na base local
            cep_formatted = f"{cep_clean[:5]}-{cep_clean[5:]}"
            
            # Verificar cache primeiro
            if cep_formatted in LocationUtils._coordinates_cache:
                return LocationUtils._coordinates_cache[cep_formatted]
            
            # 1. Tentar base de dados local (primária)
            coordinates = LocationUtils._get_coordinates_from_local_db(cep_formatted)
            
            # 2. Se não encontrar, tentar ViaCEP + salvar na base local
            if coordinates is None:
                coordinates = LocationUtils._get_coordinates_viacep_and_save(cep_formatted)
            
            # Armazenar no cache
            if coordinates:
                LocationUtils._coordinates_cache[cep_formatted] = coordinates
                logger.info(f"Coordenadas obtidas para CEP {cep}: {coordinates}")
            
            return coordinates
                
        except Exception as e:
            logger.error(f"Erro ao obter coordenadas do CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _get_coordinates_from_local_db(cep: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas da base de dados local"""
        try:
            repository, db = LocationUtils._get_cep_repository()
            
            try:
                # Buscar o CEP exato
                cep_coords = repository.get_by_cep(cep)
                
                if cep_coords:
                    logger.info(f"Coordenadas encontradas na base de dados para CEP {cep}: {cep_coords.coordinates}")
                    return cep_coords.coordinates
                
                return None
                
            finally:
                db.close()
                
        except Exception as e:
            logger.warning(f"Erro ao buscar coordenadas na base de dados para CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _get_coordinates_viacep_and_save(cep: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas via ViaCEP e salva na base local"""
        try:
            # Consulta a API do ViaCEP
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('erro') and data.get('lat') and data.get('lng'):
                    # ViaCEP retorna coordenadas diretamente
                    latitude = float(data['lat'])
                    longitude = float(data['lng'])
                    
                    # Salvar na base local para futuras consultas
                    LocationUtils._save_cep_coordinates(
                        cep=cep,
                        latitude=latitude,
                        longitude=longitude,
                        cidade=data.get('localidade'),
                        uf=data.get('uf'),
                        logradouro=data.get('logradouro'),
                        bairro=data.get('bairro')
                    )
                    
                    logger.info(f"Coordenadas obtidas via ViaCEP para CEP {cep}: ({latitude}, {longitude})")
                    return (latitude, longitude)
            
            return None
            
        except Exception as e:
            logger.warning(f"Erro ao obter dados via ViaCEP para CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _save_cep_coordinates(cep: str, latitude: float, longitude: float, 
                             cidade: Optional[str] = None, uf: Optional[str] = None,
                             logradouro: Optional[str] = None, bairro: Optional[str] = None):
        """Salva coordenadas de CEP na base local"""
        try:
            from domain.entities.cep_coordinates import CepCoordinates
            
            cep_entity = CepCoordinates(
                cep=cep,
                latitude=latitude,
                longitude=longitude,
                cidade=cidade,
                uf=uf,
                logradouro=logradouro,
                bairro=bairro
            )
            
            repository, db = LocationUtils._get_cep_repository()
            try:
                repository.create(cep_entity)
                logger.info(f"CEP {cep} salvo na base local")
            finally:
                db.close()
                
        except Exception as e:
            logger.warning(f"Erro ao salvar CEP {cep} na base local: {str(e)}")
    
    @staticmethod
    def calculate_distance(cep1: str, cep2: str) -> Optional[float]:
        """
        Calcula a distância em quilômetros entre dois CEPs
        
        Args:
            cep1: Primeiro CEP
            cep2: Segundo CEP
            
        Returns:
            Distância em quilômetros ou None se não conseguir calcular
        """
        try:
            coords1 = LocationUtils.get_coordinates_from_cep(cep1)
            coords2 = LocationUtils.get_coordinates_from_cep(cep2)
            
            if coords1 is None or coords2 is None:
                return None
            
            lat1, lon1 = coords1
            lat2, lon2 = coords2
            
            # Fórmula de Haversine para calcular distância entre coordenadas
            R = 6371  # Raio da Terra em quilômetros
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            distance = R * c
            return distance
            
        except Exception as e:
            logger.error(f"Erro ao calcular distância entre {cep1} e {cep2}: {str(e)}")
            return None
    
    @staticmethod
    def is_within_radius(cep_origin: str, cep_target: str, radius_km: float) -> bool:
        """
        Verifica se um CEP está dentro do raio especificado de outro CEP
        
        Args:
            cep_origin: CEP de origem
            cep_target: CEP de destino
            radius_km: Raio em quilômetros
            
        Returns:
            True se estiver dentro do raio, False caso contrário
        """
        distance = LocationUtils.calculate_distance(cep_origin, cep_target)
        
        if distance is None:
            return False
        
        return distance <= radius_km 