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
            # Remove caracteres não numéricos
            cep_clean = ''.join(filter(str.isdigit, cep))
            
            if len(cep_clean) != 8:
                logger.warning(f"CEP inválido: {cep}")
                return None
            
            # Verificar cache primeiro
            if cep_clean in LocationUtils._coordinates_cache:
                return LocationUtils._coordinates_cache[cep_clean]
            
            # Tentar múltiplas fontes em ordem de preferência
            coordinates = None
            
            # 1. Tentar base de dados local (mais rápido e confiável)
            coordinates = LocationUtils._get_coordinates_from_local_db(cep_clean)
            
            # 2. Se não encontrar, tentar ViaCEP + busca por endereço
            if coordinates is None:
                coordinates = LocationUtils._get_coordinates_viacep(cep_clean)
            
            # 3. Último recurso: coordenadas aproximadas por região
            if coordinates is None:
                coordinates = LocationUtils._get_approximate_coordinates(cep_clean)
            
            # Armazenar no cache
            if coordinates:
                LocationUtils._coordinates_cache[cep_clean] = coordinates
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
                # Primeiro, tentar buscar o CEP exato
                cep_coords = repository.get_by_cep(cep)
                
                if cep_coords:
                    logger.info(f"Coordenadas encontradas na base de dados para CEP {cep}: {cep_coords.coordinates}")
                    return cep_coords.coordinates
                
                # Se não encontrar, tentar buscar por prefixo
                cep_prefix = cep[:5]
                cep_list = repository.search_by_prefix(cep_prefix)
                
                if cep_list:
                    # Usar o primeiro CEP encontrado com esse prefixo
                    first_cep = cep_list[0]
                    logger.info(f"Coordenadas encontradas por prefixo para CEP {cep}: {first_cep.coordinates}")
                    return first_cep.coordinates
                
                return None
                
            finally:
                db.close()
                
        except Exception as e:
            logger.warning(f"Erro ao buscar coordenadas na base de dados para CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _get_coordinates_viacep(cep: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas usando ViaCEP + busca por endereço"""
        try:
            # Consulta a API do ViaCEP
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('erro'):
                    # Construir endereço completo
                    address_parts = []
                    if data.get('logradouro'):
                        address_parts.append(data['logradouro'])
                    if data.get('bairro'):
                        address_parts.append(data['bairro'])
                    if data.get('localidade'):
                        address_parts.append(data['localidade'])
                    if data.get('uf'):
                        address_parts.append(data['uf'])
                    
                    if address_parts:
                        full_address = ', '.join(address_parts) + ', Brazil'
                        logger.info(f"Endereço obtido via ViaCEP para CEP {cep}: {full_address}")
                        
                        # Tentar obter coordenadas do endereço via busca local
                        return LocationUtils._get_coordinates_by_address_local(full_address, cep)
            
            return None
            
        except Exception as e:
            logger.warning(f"Erro ao obter dados via ViaCEP para CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _get_coordinates_by_address_local(address: str, cep: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas usando busca local por cidade/estado"""
        try:
            # Extrair cidade e estado do endereço
            address_lower = address.lower()
            
            # Buscar por cidades conhecidas na base local
            # Removido uso de _cep_database, agora busca por cidade/uf no banco
            repository, db = LocationUtils._get_cep_repository()
            try:
                # Tentar encontrar por cidade e UF
                for city_name in [
                    'cícero dantas', 'ribeira do pombal', 'itapicuru', 'olindina', 'acajutiba',
                    'crisópolis', 'esplanada', 'cardeal da silva', 'conde', 'entre rios',
                    'são paulo', 'campinas', 'santos', 'rio de janeiro', 'porto alegre',
                    'salvador', 'belo horizonte', 'recife', 'fortaleza', 'brasília', 'curitiba'
                ]:
                    if city_name in address_lower:
                        # Buscar todos os CEPs dessa cidade
                        results = repository.get_by_cidade_uf(city_name.title(), None)
                        if results:
                            logger.info(f"Coordenadas encontradas por cidade para CEP {cep}: {results[0].coordinates}")
                            return results[0].coordinates
                return None
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Erro ao obter coordenadas por endereço para CEP {cep}: {str(e)}")
            return None
    
    @staticmethod
    def _get_approximate_coordinates(cep: str) -> Tuple[float, float]:
        """
        Obtém coordenadas aproximadas baseadas no CEP
        Esta é uma implementação simplificada - em produção, seria melhor usar
        uma base de dados de CEPs com coordenadas precisas
        """
        # Mapeamento simplificado de CEPs para coordenadas aproximadas
        # Em produção, isso deveria ser uma base de dados completa
        cep_prefix = cep[:5]
        
        # Coordenadas aproximadas por região
        if cep.startswith('48100'):  # Cícero Dantas - BA
            return (-10.6000, -38.3833)
        elif cep.startswith('48400'):  # Ribeira do Pombal - BA
            return (-10.8333, -38.5333)
        elif cep.startswith('48120'):  # Itapicuru - BA
            return (-11.3167, -38.2333)
        elif cep.startswith('48130'):  # Olindina - BA
            return (-11.3667, -38.3333)
        elif cep.startswith('48140'):  # Acajutiba - BA
            return (-11.6667, -38.0167)
        elif cep.startswith('48150'):  # Crisópolis - BA
            return (-11.5167, -38.1500)
        elif cep.startswith('01000'):  # São Paulo capital
            return (-23.5505, -46.6333)
        elif cep.startswith('02000'):  # Campinas - SP
            return (-22.9064, -47.0616)
        elif cep.startswith('03000'):  # Santos - SP
            return (-23.9608, -46.3336)
        elif cep.startswith('04000'):  # São Paulo capital
            return (-23.5505, -46.6333)
        elif cep.startswith('05000'):  # São Paulo capital
            return (-23.5505, -46.6333)
        elif cep.startswith('06000'):  # São Paulo capital
            return (-23.5505, -46.6333)
        elif cep.startswith('07000'):  # Rio de Janeiro
            return (-22.9068, -43.1729)
        elif cep.startswith('08000'):  # Porto Alegre
            return (-30.0346, -51.2177)
        elif cep.startswith('09000'):  # Salvador
            return (-12.9714, -38.5011)
        else:
            # Coordenadas padrão (São Paulo)
            return (-23.5505, -46.6333)
    
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