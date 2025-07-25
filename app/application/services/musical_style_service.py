from typing import List, Optional
from domain.entities.musical_style import MusicalStyle
from domain.repositories.musical_style_repository import MusicalStyleRepository
from app.schemas.musical_style import MusicalStyleCreate, MusicalStyleUpdate, MusicalStyleResponse

class MusicalStyleService:
    def __init__(self, musical_style_repository: MusicalStyleRepository):
        self.musical_style_repository = musical_style_repository

    def create_musical_style(self, style_data: MusicalStyleCreate) -> MusicalStyleResponse:
        existing = self.musical_style_repository.get_by_estyle(style_data.style)
        if existing:
            raise ValueError("Estilo musical já existe.")
        style = MusicalStyle(estyle=style_data.style)
        created = self.musical_style_repository.create(style)
        return MusicalStyleResponse(
            id=created.id,
            style=created.estyle,
            created_at=created.created_at,
            updated_at=created.updated_at
        )

    def get_musical_styles(self, skip: int = 0, limit: int = 100) -> List[MusicalStyleResponse]:
        styles = self.musical_style_repository.get_all(skip=skip, limit=limit)
        return [
            MusicalStyleResponse(
                id=s.id,
                style=s.estyle,
                created_at=s.created_at,
                updated_at=s.updated_at
            ) for s in styles
        ]

    def get_musical_style_by_id(self, style_id: int) -> Optional[MusicalStyleResponse]:
        s = self.musical_style_repository.get_by_id(style_id)
        if not s:
            return None
        return MusicalStyleResponse(
            id=s.id,
            style=s.estyle,
            created_at=s.created_at,
            updated_at=s.updated_at
        )

    def update_musical_style(self, style_id: int, style_data: MusicalStyleUpdate) -> Optional[MusicalStyleResponse]:
        s = self.musical_style_repository.get_by_id(style_id)
        if not s:
            return None
        if style_data.style is not None:
            existing = self.musical_style_repository.get_by_estyle(style_data.style)
            if existing and existing.id != style_id:
                raise ValueError("Estilo musical já existe.")
            s.estyle = style_data.style
        updated = self.musical_style_repository.update(s)
        return MusicalStyleResponse(
            id=updated.id,
            style=updated.estyle,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )

    def delete_musical_style(self, style_id: int) -> bool:
        return self.musical_style_repository.delete(style_id) 