from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.musical_style import MusicalStyle
from domain.repositories.musical_style_repository import MusicalStyleRepository
from infrastructure.database.models.musical_style_model import MusicalStyleModel

class MusicalStyleRepositoryImpl(MusicalStyleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, musical_style: MusicalStyle) -> MusicalStyle:
        db_style = MusicalStyleModel(estyle=musical_style.estyle)
        self.session.add(db_style)
        self.session.commit()
        self.session.refresh(db_style)
        return MusicalStyle(
            id=db_style.id,
            estyle=db_style.estyle,
            created_at=db_style.created_at,
            updated_at=db_style.updated_at
        )

    def get_by_id(self, musical_style_id: int) -> Optional[MusicalStyle]:
        db_style = self.session.query(MusicalStyleModel).filter(MusicalStyleModel.id == musical_style_id).first()
        if not db_style:
            return None
        return MusicalStyle(
            id=db_style.id,
            estyle=db_style.estyle,
            created_at=db_style.created_at,
            updated_at=db_style.updated_at
        )

    def get_by_estyle(self, estyle: str) -> Optional[MusicalStyle]:
        db_style = self.session.query(MusicalStyleModel).filter(MusicalStyleModel.estyle == estyle).first()
        if not db_style:
            return None
        return MusicalStyle(
            id=db_style.id,
            estyle=db_style.estyle,
            created_at=db_style.created_at,
            updated_at=db_style.updated_at
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[MusicalStyle]:
        db_styles = self.session.query(MusicalStyleModel).offset(skip).limit(limit).all()
        return [
            MusicalStyle(
                id=db_style.id,
                estyle=db_style.estyle,
                created_at=db_style.created_at,
                updated_at=db_style.updated_at
            )
            for db_style in db_styles
        ]

    def update(self, musical_style: MusicalStyle) -> MusicalStyle:
        db_style = self.session.query(MusicalStyleModel).filter(MusicalStyleModel.id == musical_style.id).first()
        if not db_style:
            raise ValueError("Estilo musical não encontrado")
        db_style.estyle = musical_style.estyle
        db_style.updated_at = musical_style.updated_at
        self.session.commit()
        self.session.refresh(db_style)
        return MusicalStyle(
            id=db_style.id,
            estyle=db_style.estyle,
            created_at=db_style.created_at,
            updated_at=db_style.updated_at
        )

    def delete(self, musical_style_id: int) -> bool:
        db_style = self.session.query(MusicalStyleModel).filter(MusicalStyleModel.id == musical_style_id).first()
        if not db_style:
            return False
        self.session.delete(db_style)
        self.session.commit()
        return True 