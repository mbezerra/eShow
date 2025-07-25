from typing import Optional, List
from sqlalchemy.orm import Session
from domain.repositories.cep_coordinates_repository import CepCoordinatesRepository
from domain.entities.cep_coordinates import CepCoordinates
from infrastructure.database.models.cep_coordinates_model import CepCoordinatesModel

class CepCoordinatesRepositoryImpl(CepCoordinatesRepository):
    """Implementação do repositório de coordenadas de CEPs"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_cep(self, cep: str) -> Optional[CepCoordinates]:
        """Obtém coordenadas por CEP"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cep == cep
        ).first()
        
        if model:
            return CepCoordinates(
                cep=model.cep,
                latitude=model.latitude,
                longitude=model.longitude,
                cidade=model.cidade,
                uf=model.uf,
                logradouro=model.logradouro,
                bairro=model.bairro,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        return None
    
    def get_by_cidade_uf(self, cidade: str, uf: str) -> List[CepCoordinates]:
        """Obtém coordenadas por cidade e UF"""
        models = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cidade == cidade,
            CepCoordinatesModel.uf == uf
        ).all()
        
        return [
            CepCoordinates(
                cep=model.cep,
                latitude=model.latitude,
                longitude=model.longitude,
                cidade=model.cidade,
                uf=model.uf,
                logradouro=model.logradouro,
                bairro=model.bairro,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    
    def create(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Cria novo registro de coordenadas"""
        model = CepCoordinatesModel(
            cep=cep_coordinates.cep,
            latitude=cep_coordinates.latitude,
            longitude=cep_coordinates.longitude,
            cidade=cep_coordinates.cidade,
            uf=cep_coordinates.uf,
            logradouro=cep_coordinates.logradouro,
            bairro=cep_coordinates.bairro
        )
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return CepCoordinates(
            cep=model.cep,
            latitude=model.latitude,
            longitude=model.longitude,
            cidade=model.cidade,
            uf=model.uf,
            logradouro=model.logradouro,
            bairro=model.bairro,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def update(self, cep_coordinates: CepCoordinates) -> CepCoordinates:
        """Atualiza registro de coordenadas"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cep == cep_coordinates.cep
        ).first()
        
        if not model:
            raise ValueError(f"CEP {cep_coordinates.cep} não encontrado")
        
        model.latitude = cep_coordinates.latitude
        model.longitude = cep_coordinates.longitude
        model.cidade = cep_coordinates.cidade
        model.uf = cep_coordinates.uf
        model.logradouro = cep_coordinates.logradouro
        model.bairro = cep_coordinates.bairro
        
        self.db.commit()
        self.db.refresh(model)
        
        return CepCoordinates(
            cep=model.cep,
            latitude=model.latitude,
            longitude=model.longitude,
            cidade=model.cidade,
            uf=model.uf,
            logradouro=model.logradouro,
            bairro=model.bairro,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def delete(self, cep: str) -> bool:
        """Deleta registro de coordenadas"""
        model = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cep == cep
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
                cep=model.cep,
                latitude=model.latitude,
                longitude=model.longitude,
                cidade=model.cidade,
                uf=model.uf,
                logradouro=model.logradouro,
                bairro=model.bairro,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
    
    def search_by_prefix(self, cep_prefix: str) -> List[CepCoordinates]:
        """Busca CEPs por prefixo"""
        models = self.db.query(CepCoordinatesModel).filter(
            CepCoordinatesModel.cep.like(f"{cep_prefix}%")
        ).all()
        
        return [
            CepCoordinates(
                cep=model.cep,
                latitude=model.latitude,
                longitude=model.longitude,
                cidade=model.cidade,
                uf=model.uf,
                logradouro=model.logradouro,
                bairro=model.bairro,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ] 