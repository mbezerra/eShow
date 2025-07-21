from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.artist_type import ArtistType, ArtistTypeEnum
from domain.repositories.artist_type_repository import ArtistTypeRepository
from infrastructure.database.models.artist_type_model import ArtistTypeModel

class ArtistTypeRepositoryImpl(ArtistTypeRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, artist_type: ArtistType) -> ArtistType:
        db_artist_type = ArtistTypeModel(tipo=artist_type.tipo)
        self.session.add(db_artist_type)
        self.session.commit()
        self.session.refresh(db_artist_type)
        return ArtistType(
            id=db_artist_type.id,
            tipo=db_artist_type.tipo,
            created_at=db_artist_type.created_at,
            updated_at=db_artist_type.updated_at
        )

    def get_by_id(self, artist_type_id: int) -> Optional[ArtistType]:
        db_artist_type = self.session.query(ArtistTypeModel).filter(ArtistTypeModel.id == artist_type_id).first()
        if not db_artist_type:
            return None
        return ArtistType(
            id=db_artist_type.id,
            tipo=db_artist_type.tipo,
            created_at=db_artist_type.created_at,
            updated_at=db_artist_type.updated_at
        )

    def get_by_tipo(self, tipo: ArtistTypeEnum) -> Optional[ArtistType]:
        db_artist_type = self.session.query(ArtistTypeModel).filter(ArtistTypeModel.tipo == tipo).first()
        if not db_artist_type:
            return None
        return ArtistType(
            id=db_artist_type.id,
            tipo=db_artist_type.tipo,
            created_at=db_artist_type.created_at,
            updated_at=db_artist_type.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ArtistType]:
        db_artist_types = self.session.query(ArtistTypeModel).offset(skip).limit(limit).all()
        return [
            ArtistType(
                id=db_artist_type.id,
                tipo=db_artist_type.tipo,
                created_at=db_artist_type.created_at,
                updated_at=db_artist_type.updated_at
            )
            for db_artist_type in db_artist_types
        ]

    def update(self, artist_type: ArtistType) -> ArtistType:
        db_artist_type = self.session.query(ArtistTypeModel).filter(ArtistTypeModel.id == artist_type.id).first()
        if not db_artist_type:
            raise ValueError("Tipo de artista não encontrado")
        db_artist_type.tipo = artist_type.tipo
        db_artist_type.updated_at = artist_type.updated_at
        self.session.commit()
        self.session.refresh(db_artist_type)
        return ArtistType(
            id=db_artist_type.id,
            tipo=db_artist_type.tipo,
            created_at=db_artist_type.created_at,
            updated_at=db_artist_type.updated_at
        )

    def delete(self, artist_type_id: int) -> bool:
        db_artist_type = self.session.query(ArtistTypeModel).filter(ArtistTypeModel.id == artist_type_id).first()
        if not db_artist_type:
            return False
        self.session.delete(db_artist_type)
        self.session.commit()
        return True 