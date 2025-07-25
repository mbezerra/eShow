from typing import Optional, List
from sqlalchemy.orm import Session
from domain.repositories.cep_coordinates_repository import CepCoordinatesRepository
from domain.entities.cep_coordinates import CepCoordinates
from infrastructure.database.models.cep_coordinates_model import CepCoordinatesModel
import unicodedata
import logging

logger = logging.getLogger(__name__)

class CepCoordinatesRepositoryImpl(CepCoordinatesRepository):
    """Implementação do repositório de coordenadas de municípios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_cidade_uf(self, cidade: str, uf: str) -> Optional[CepCoordinates]:
        """
        Obtém coordenadas por cidade e UF - ignora acentuação
        
        Args:
            cidade: Nome da cidade (será normalizado)
            uf: Sigla da UF (2 caracteres)
            
        Returns:
            Coordenadas encontradas ou None
        """
        try:
            # Normalizar cidade removendo acentos
            cidade_normalizada = self._normalize_text(cidade)
            uf_clean = uf.strip().upper()
            
            # Buscar por cidade normalizada e UF
            model = self.db.query(CepCoordinatesModel).filter(
                CepCoordinatesModel.cidade_normalizada == cidade_normalizada,
                CepCoordinatesModel.uf == uf_clean
            ).first()
            
            if model:
                return CepCoordinates(
                    cidade=model.cidade,
                    uf=model.uf,
                    latitude=model.latitude,
                    longitude=model.longitude,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cidade '{cidade}'/UF '{uf}': {str(e)}")
            return None
    
    def get_by_uf(self, uf: str) -> List[CepCoordinates]:
        """Obtém coordenadas por UF"""
        models = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.uf == uf
        ).all()
        
        return [
            CepCoordinates(
                cidade=model.cidade,
                uf=model.uf,
                latitude=model.latitude,
                longitude=model.longitude,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    
    def create(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Cria novo registro de coordenadas"""
        model = CepCoordinatesModel(
            cidade=cep_coordinates.cidade,
            uf=cep_coordinates.uf,
            latitude=cep_coordinates.latitude,
            longitude=cep_coordinates.longitude
        )
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return CepCoordinates(
            cidade=model.cidade,
            uf=model.uf,
            latitude=model.latitude,
            longitude=model.longitude,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def update(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Atualiza registro de coordenadas"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cidade == cep_coordinates.cidade,
            CepCoordinatesModel.uf == cep_coordinates.uf
        ).first()
        
        if not model:
            raise ValueError(f"Município {cep_coordinates.cidade}/{cep_coordinates.uf} não encontrado")
        
        model.latitude = cep_coordinates.latitude
        model.longitude = cep_coordinates.longitude
        
        self.db.commit()
        self.db.refresh(model)
        
        return CepCoordinates(
            cidade=model.cidade,
            uf=model.uf,
            latitude=model.latitude,
            longitude=model.longitude,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def delete(self, cidade: str, uf: str) -> bool:
        """Deleta registro de coordenadas"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cidade == cidade,
            CepCoordinatesModel.uf == uf
        ).first()
        
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False
    
    def get_all(self) -> List[CepCoordinates]:
        """Obtém todas as coordenadas"""
        models = self.db.query(CepCoordinatesModel).all()
        
        return [
            CepCoordinates(
                cidade=model.cidade,
                uf=model.uf,
                latitude=model.latitude,
                longitude=model.longitude,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    
    def search_by_cidade(self, cidade: str) -> List[CepCoordinates]:
        """
        Busca municípios por nome da cidade (parcial) - ignora acentuação
        
        Args:
            cidade: Nome da cidade para buscar (será normalizado)
            
        Returns:
            Lista de coordenadas encontradas
        """
        try:
            # Normalizar cidade removendo acentos
            cidade_normalizada = self._normalize_text(cidade)
            
            # Buscar cidades que contenham o nome normalizado
            models = self.db.query(CepCoordinatesModel).filter(
                CepCoordinatesModel.cidade_normalizada.like(f"%{cidade_normalizada}%")
            ).limit(20).all()
            
            return [
                CepCoordinates(
                    cidade=model.cidade,
                    uf=model.uf,
                    latitude=model.latitude,
                    longitude=model.longitude,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in models
            ]
            
        except Exception as e:
            logger.error(f"Erro ao buscar cidade '{cidade}': {str(e)}")
            return []
    
    def _normalize_text(self, text: str) -> str:
        """
        Normaliza texto removendo acentos e convertendo para maiúsculas
        
        Args:
            text: Texto a ser normalizado
            
        Returns:
            Texto normalizado sem acentos e em maiúsculas
        """
        if not text:
            return ""
        # Remove acentos usando unicodedata
        normalized = unicodedata.normalize('NFD', text)
        # Remove caracteres de acentuação
        ascii_text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        # Converte para maiúsculas e remove espaços extras
        return ascii_text.strip().upper()
    
    def get_nearby_cities(self, latitude: float, longitude: float, radius_km: float = 50) -> List[CepCoordinates]:
        """Busca cidades próximas usando fórmula de Haversine"""
        # Fórmula de Haversine para calcular distância
        # Esta é uma aproximação simples - para produção, considere usar PostGIS ou similar
        models = self.db.query(CepCoordinatesModel).all()
        
        nearby_cities = []
        for model in models:
            # Cálculo simplificado de distância (aproximação)
            lat_diff = abs(model.latitude - latitude)
            lng_diff = abs(model.longitude - longitude)
            
            # Aproximação: 1 grau ≈ 111 km
            distance_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
            
            if distance_km <= radius_km:
                nearby_cities.append(CepCoordinates(
                    cidade=model.cidade,
                    uf=model.uf,
                    latitude=model.latitude,
                    longitude=model.longitude,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                ))
        
        return nearby_cities 