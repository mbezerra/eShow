from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.space_type import SpaceType
from domain.repositories.space_type_repository import SpaceTypeRepository
from infrastructure.database.models.space_type_model import SpaceTypeModel

class SpaceTypeRepositoryImpl(SpaceTypeRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, space_type: SpaceType) -> SpaceType:
        db_space_type = SpaceTypeModel(
            tipo=space_type.tipo
        )
        self.db.add(db_space_type)
        self.db.commit()
        self.db.refresh(db_space_type)
        return SpaceType(
            id=db_space_type.id,
            tipo=db_space_type.tipo,
            created_at=db_space_type.created_at,
            updated_at=db_space_type.updated_at
        )
    
    def get_by_id(self, space_type_id: int) -> Optional[SpaceType]:
        db_space_type = self.db.query(SpaceTypeModel).filter(SpaceTypeModel.id == space_type_id).first()
        if db_space_type is None:
            return None
        return SpaceType(
            id=db_space_type.id,
            tipo=db_space_type.tipo,
            created_at=db_space_type.created_at,
            updated_at=db_space_type.updated_at
        )
    
    def get_by_tipo(self, tipo: str) -> Optional[SpaceType]:
        db_space_type = self.db.query(SpaceTypeModel).filter(SpaceTypeModel.tipo == tipo).first()
        if db_space_type is None:
            return None
        return SpaceType(
            id=db_space_type.id,
            tipo=db_space_type.tipo,
            created_at=db_space_type.created_at,
            updated_at=db_space_type.updated_at
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpaceType]:
        db_space_types = self.db.query(SpaceTypeModel).offset(skip).limit(limit).all()
        return [
            SpaceType(
                id=db_space_type.id,
                tipo=db_space_type.tipo,
                created_at=db_space_type.created_at,
                updated_at=db_space_type.updated_at
            )
            for db_space_type in db_space_types
        ]
    
    def update(self, space_type: SpaceType) -> SpaceType:
        db_space_type = self.db.query(SpaceTypeModel).filter(SpaceTypeModel.id == space_type.id).first()
        if db_space_type is None:
            raise ValueError(f"SpaceType with id {space_type.id} not found")
        
        db_space_type.tipo = space_type.tipo
        self.db.commit()
        self.db.refresh(db_space_type)
        
        return SpaceType(
            id=db_space_type.id,
            tipo=db_space_type.tipo,
            created_at=db_space_type.created_at,
            updated_at=db_space_type.updated_at
        )
    
    def delete(self, space_type_id: int) -> bool:
        db_space_type = self.db.query(SpaceTypeModel).filter(SpaceTypeModel.id == space_type_id).first()
        if db_space_type is None:
            return False
        
        self.db.delete(db_space_type)
        self.db.commit()
        return True 