from typing import List, Optional
from domain.entities.space_type import SpaceType
from domain.repositories.space_type_repository import SpaceTypeRepository

class SpaceTypeService:
    def __init__(self, space_type_repository: SpaceTypeRepository):
        self.space_type_repository = space_type_repository
    
    def create_space_type(self, tipo: str) -> SpaceType:
        # Verificar se já existe um space type com este tipo
        existing_space_type = self.space_type_repository.get_by_tipo(tipo)
        if existing_space_type:
            raise ValueError(f"SpaceType with tipo '{tipo}' already exists")
        
        space_type = SpaceType(tipo=tipo)
        return self.space_type_repository.create(space_type)
    
    def get_space_type_by_id(self, space_type_id: int) -> Optional[SpaceType]:
        return self.space_type_repository.get_by_id(space_type_id)
    
    def get_space_type_by_tipo(self, tipo: str) -> Optional[SpaceType]:
        return self.space_type_repository.get_by_tipo(tipo)
    
    def get_all_space_types(self, skip: int = 0, limit: int = 100) -> List[SpaceType]:
        return self.space_type_repository.get_all(skip=skip, limit=limit)
    
    def update_space_type(self, space_type_id: int, tipo: str) -> SpaceType:
        space_type = self.space_type_repository.get_by_id(space_type_id)
        if not space_type:
            raise ValueError(f"SpaceType with id {space_type_id} not found")
        
        # Verificar se já existe outro space type com este tipo
        existing_space_type = self.space_type_repository.get_by_tipo(tipo)
        if existing_space_type and existing_space_type.id != space_type_id:
            raise ValueError(f"SpaceType with tipo '{tipo}' already exists")
        
        space_type.tipo = tipo
        return self.space_type_repository.update(space_type)
    
    def delete_space_type(self, space_type_id: int) -> bool:
        return self.space_type_repository.delete(space_type_id) 