from typing import List, Optional
from domain.entities.festival_type import FestivalType
from domain.repositories.festival_type_repository import FestivalTypeRepository

class FestivalTypeService:
    def __init__(self, festival_type_repository: FestivalTypeRepository):
        self.festival_type_repository = festival_type_repository

    def create_festival_type(self, type: str) -> FestivalType:
        # Verificar se já existe um festival type com este type
        existing_festival_type = self.festival_type_repository.get_by_type(type)
        if existing_festival_type:
            raise ValueError(f"FestivalType with type '{type}' already exists")

        festival_type = FestivalType(type=type)
        return self.festival_type_repository.create(festival_type)

    def get_festival_type_by_id(self, festival_type_id: int) -> Optional[FestivalType]:
        return self.festival_type_repository.get_by_id(festival_type_id)

    def get_festival_type_by_type(self, type: str) -> Optional[FestivalType]:
        return self.festival_type_repository.get_by_type(type)

    def get_all_festival_types(self, skip: int = 0, limit: int = 100) -> List[FestivalType]:
        return self.festival_type_repository.get_all(skip=skip, limit=limit)

    def update_festival_type(self, festival_type_id: int, type: str) -> FestivalType:
        festival_type = self.festival_type_repository.get_by_id(festival_type_id)
        if not festival_type:
            raise ValueError(f"FestivalType with id {festival_type_id} not found")

        # Verificar se já existe outro festival type com este type
        existing_festival_type = self.festival_type_repository.get_by_type(type)
        if existing_festival_type and existing_festival_type.id != festival_type_id:
            raise ValueError(f"FestivalType with type '{type}' already exists")

        festival_type.type = type
        return self.festival_type_repository.update(festival_type)

    def delete_festival_type(self, festival_type_id: int) -> bool:
        return self.festival_type_repository.delete(festival_type_id) 