from typing import Optional, List
from sqlalchemy.orm import Session
from domain.repositories.cep_coordinates_repository import CepCoordinatesRepository
from domain.entities.cep_coordinates import CepCoordinates
from infrastructure.database.models.cep_coordinates_model import CepCoordinatesModel

class CepCoordinatesRepositoryImpl(CepCoordinatesRepository):
    """Implementação do repositório de coordenadas de municípios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_cidade_uf(self, cidade: str, uf: str) -> Optional[CepCoordinates]:
        """Obtém coordenadas por cidade e UF"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cidade == cidade,
            CepCoordinatesModel.uf == uf
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
        """Busca municípios por nome da cidade (parcial)"""
        models = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cidade.like(f"%{cidade}%")
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