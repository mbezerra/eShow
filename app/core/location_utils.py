import requests
import math
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class LocationUtils:
    """Utilitário para cálculos de localização e distância"""
    
    @staticmethod
    def get_coordinates_from_cep(cep: str) -> Optional[Tuple[float, float]]:
        """
        Obtém as coordenadas (latitude, longitude) de um CEP usando a API do ViaCEP
        
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
            
            # Consulta a API do ViaCEP
            url = f"https://viacep.com.br/ws/{cep_clean}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('erro'):
                    # Extrai latitude e longitude do campo 'ibge'
                    # Como o ViaCEP não retorna coordenadas diretamente,
                    # vamos usar uma abordagem alternativa
                    # Por enquanto, vamos retornar coordenadas aproximadas baseadas no CEP
                    return LocationUtils._get_approximate_coordinates(cep_clean)
                else:
                    logger.warning(f"CEP não encontrado: {cep}")
                    return None
            else:
                logger.error(f"Erro ao consultar CEP {cep}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao obter coordenadas do CEP {cep}: {str(e)}")
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
        
        # Coordenadas aproximadas por região (exemplo)
        # São Paulo capital: -23.5505, -46.6333
        # Rio de Janeiro: -22.9068, -43.1729
        # Belo Horizonte: -19.9167, -43.9345
        # etc.
        
        # Por enquanto, vamos usar coordenadas fixas para demonstração
        # Em produção, isso deveria ser uma consulta a uma base de dados
        return (-23.5505, -46.6333)  # São Paulo como padrão
    
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