from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.festival_type import FestivalType
from domain.repositories.festival_type_repository import FestivalTypeRepository
from infrastructure.database.models.festival_type_model import FestivalTypeModel

class FestivalTypeRepositoryImpl(FestivalTypeRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, festival_type: FestivalType) -> FestivalType:
        db_festival_type = FestivalTypeModel(
            type=festival_type.type
        )
        self.db.add(db_festival_type)
        self.db.commit()
        self.db.refresh(db_festival_type)
        return FestivalType(
            id=db_festival_type.id,
            type=db_festival_type.type,
            created_at=db_festival_type.created_at,
            updated_at=db_festival_type.updated_at
        )

    def get_by_id(self, festival_type_id: int) -> Optional[FestivalType]:
        db_festival_type = self.db.query(FestivalTypeModel).filter(FestivalTypeModel.id == festival_type_id).first()
        if db_festival_type is None:
            return None
        return FestivalType(
            id=db_festival_type.id,
            type=db_festival_type.type,
            created_at=db_festival_type.created_at,
            updated_at=db_festival_type.updated_at
        )

    def get_by_type(self, type: str) -> Optional[FestivalType]:
        db_festival_type = self.db.query(FestivalTypeModel).filter(FestivalTypeModel.type == type).first()
        if db_festival_type is None:
            return None
        return FestivalType(
            id=db_festival_type.id,
            type=db_festival_type.type,
            created_at=db_festival_type.created_at,
            updated_at=db_festival_type.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[FestivalType]:
        db_festival_types = self.db.query(FestivalTypeModel).offset(skip).limit(limit).all()
        return [
            FestivalType(
                id=db_festival_type.id,
                type=db_festival_type.type,
                created_at=db_festival_type.created_at,
                updated_at=db_festival_type.updated_at
            )
            for db_festival_type in db_festival_types
        ]

    def update(self, festival_type: FestivalType) -> FestivalType:
        db_festival_type = self.db.query(FestivalTypeModel).filter(FestivalTypeModel.id == festival_type.id).first()
        if db_festival_type is None:
            raise ValueError(f"FestivalType with id {festival_type.id} not found")

        db_festival_type.type = festival_type.type
        self.db.commit()
        self.db.refresh(db_festival_type)

        return FestivalType(
            id=db_festival_type.id,
            type=db_festival_type.type,
            created_at=db_festival_type.created_at,
            updated_at=db_festival_type.updated_at
        )

    def delete(self, festival_type_id: int) -> bool:
        db_festival_type = self.db.query(FestivalTypeModel).filter(FestivalTypeModel.id == festival_type_id).first()
        if db_festival_type is None:
            return False

        self.db.delete(db_festival_type)
        self.db.commit()
        return True 