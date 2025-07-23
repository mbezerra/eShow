from typing import List, Optional
from domain.repositories.space_festival_type_repository import SpaceFestivalTypeRepository
from domain.entities.space_festival_type import SpaceFestivalType
from app.schemas.space_festival_type import SpaceFestivalTypeCreate, SpaceFestivalTypeUpdate

class SpaceFestivalTypeService:
    """Serviço de aplicação para o relacionamento N:N entre Spaces e Festival Types"""
    
    def __init__(self, space_festival_type_repository: SpaceFestivalTypeRepository):
        self.space_festival_type_repository = space_festival_type_repository
    
    def create_space_festival_type(self, space_festival_type_data: SpaceFestivalTypeCreate) -> SpaceFestivalType:
        """Criar um novo relacionamento entre espaço e tipo de festival"""
        space_festival_type = SpaceFestivalType(
            space_id=space_festival_type_data.space_id,
            festival_type_id=space_festival_type_data.festival_type_id,
            tema=space_festival_type_data.tema,
            descricao=space_festival_type_data.descricao,
            link_divulgacao=space_festival_type_data.link_divulgacao,
            banner=space_festival_type_data.banner,
            data=space_festival_type_data.data,
            horario=space_festival_type_data.horario
        )
        
        return self.space_festival_type_repository.create(space_festival_type)
    
    def get_space_festival_type_by_id(self, space_festival_type_id: int) -> Optional[SpaceFestivalType]:
        """Obter um relacionamento por ID"""
        return self.space_festival_type_repository.get_by_id(space_festival_type_id)
    
    def get_festival_types_by_space(self, space_id: int) -> List[SpaceFestivalType]:
        """Obter todos os tipos de festivais de um espaço"""
        return self.space_festival_type_repository.get_by_space_id(space_id)
    
    def get_spaces_by_festival_type(self, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter todos os espaços de um tipo de festival"""
        return self.space_festival_type_repository.get_by_festival_type_id(festival_type_id)
    
    def get_space_festival_types_by_space_and_festival_type(self, space_id: int, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter relacionamentos específicos entre espaço e tipo de festival"""
        return self.space_festival_type_repository.get_by_space_and_festival_type(space_id, festival_type_id)
    
    def update_space_festival_type(self, space_festival_type_id: int, space_festival_type_data: SpaceFestivalTypeUpdate) -> Optional[SpaceFestivalType]:
        """Atualizar um relacionamento"""
        # Obter o relacionamento atual
        existing = self.space_festival_type_repository.get_by_id(space_festival_type_id)
        if not existing:
            return None
        
        # Criar entidade com os dados atualizados
        updated_space_festival_type = SpaceFestivalType(
            id=existing.id,
            space_id=existing.space_id,
            festival_type_id=existing.festival_type_id,
            tema=space_festival_type_data.tema if space_festival_type_data.tema is not None else existing.tema,
            descricao=space_festival_type_data.descricao if space_festival_type_data.descricao is not None else existing.descricao,
            link_divulgacao=space_festival_type_data.link_divulgacao if space_festival_type_data.link_divulgacao is not None else existing.link_divulgacao,
            banner=space_festival_type_data.banner if space_festival_type_data.banner is not None else existing.banner,
            data=space_festival_type_data.data if space_festival_type_data.data is not None else existing.data,
            horario=space_festival_type_data.horario if space_festival_type_data.horario is not None else existing.horario,
            created_at=existing.created_at
        )
        
        return self.space_festival_type_repository.update(space_festival_type_id, updated_space_festival_type)
    
    def delete_space_festival_type(self, space_festival_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        return self.space_festival_type_repository.delete(space_festival_type_id)
    
    def delete_all_space_festival_types_by_space(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        return self.space_festival_type_repository.delete_by_space_id(space_id)
    
    def delete_all_space_festival_types_by_festival_type(self, festival_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de festival"""
        return self.space_festival_type_repository.delete_by_festival_type_id(festival_type_id)
    
    def get_all_space_festival_types(self) -> List[SpaceFestivalType]:
        """Obter todos os relacionamentos"""
        return self.space_festival_type_repository.get_all() 