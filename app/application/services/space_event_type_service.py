from typing import List, Optional
from domain.repositories.space_event_type_repository import SpaceEventTypeRepository
from domain.entities.space_event_type import SpaceEventType
from app.schemas.space_event_type import SpaceEventTypeCreate, SpaceEventTypeUpdate

class SpaceEventTypeService:
    """Serviço de aplicação para o relacionamento N:N entre Spaces e Event Types"""
    
    def __init__(self, space_event_type_repository: SpaceEventTypeRepository):
        self.space_event_type_repository = space_event_type_repository
    
    def create_space_event_type(self, space_event_type_data: SpaceEventTypeCreate) -> SpaceEventType:
        """Criar um novo relacionamento entre espaço e tipo de evento"""
        space_event_type = SpaceEventType(
            space_id=space_event_type_data.space_id,
            event_type_id=space_event_type_data.event_type_id,
            tema=space_event_type_data.tema,
            descricao=space_event_type_data.descricao,
            link_divulgacao=space_event_type_data.link_divulgacao,
            banner=space_event_type_data.banner,
            data=space_event_type_data.data,
            horario=space_event_type_data.horario
        )
        
        return self.space_event_type_repository.create(space_event_type)
    
    def get_space_event_type_by_id(self, space_event_type_id: int) -> Optional[SpaceEventType]:
        """Obter um relacionamento por ID"""
        return self.space_event_type_repository.get_by_id(space_event_type_id)
    
    def get_event_types_by_space(self, space_id: int) -> List[SpaceEventType]:
        """Obter todos os tipos de eventos de um espaço"""
        return self.space_event_type_repository.get_by_space_id(space_id)
    
    def get_spaces_by_event_type(self, event_type_id: int) -> List[SpaceEventType]:
        """Obter todos os espaços de um tipo de evento"""
        return self.space_event_type_repository.get_by_event_type_id(event_type_id)
    
    def get_space_event_types_by_space_and_event_type(self, space_id: int, event_type_id: int) -> List[SpaceEventType]:
        """Obter relacionamentos específicos entre espaço e tipo de evento"""
        return self.space_event_type_repository.get_by_space_and_event_type(space_id, event_type_id)
    
    def update_space_event_type(self, space_event_type_id: int, space_event_type_data: SpaceEventTypeUpdate) -> Optional[SpaceEventType]:
        """Atualizar um relacionamento"""
        # Obter o relacionamento atual
        existing = self.space_event_type_repository.get_by_id(space_event_type_id)
        if not existing:
            return None
        
        # Criar entidade com os dados atualizados
        updated_space_event_type = SpaceEventType(
            id=existing.id,
            space_id=existing.space_id,
            event_type_id=existing.event_type_id,
            tema=space_event_type_data.tema if space_event_type_data.tema is not None else existing.tema,
            descricao=space_event_type_data.descricao if space_event_type_data.descricao is not None else existing.descricao,
            link_divulgacao=space_event_type_data.link_divulgacao if space_event_type_data.link_divulgacao is not None else existing.link_divulgacao,
            banner=space_event_type_data.banner if space_event_type_data.banner is not None else existing.banner,
            data=space_event_type_data.data if space_event_type_data.data is not None else existing.data,
            horario=space_event_type_data.horario if space_event_type_data.horario is not None else existing.horario,
            created_at=existing.created_at
        )
        
        return self.space_event_type_repository.update(space_event_type_id, updated_space_event_type)
    
    def delete_space_event_type(self, space_event_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        return self.space_event_type_repository.delete(space_event_type_id)
    
    def delete_all_space_event_types_by_space(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        return self.space_event_type_repository.delete_by_space_id(space_id)
    
    def delete_all_space_event_types_by_event_type(self, event_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de evento"""
        return self.space_event_type_repository.delete_by_event_type_id(event_type_id)
    
    def get_all_space_event_types(self) -> List[SpaceEventType]:
        """Obter todos os relacionamentos"""
        return self.space_event_type_repository.get_all() 