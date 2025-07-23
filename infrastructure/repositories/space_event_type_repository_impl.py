from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories.space_event_type_repository import SpaceEventTypeRepository
from domain.entities.space_event_type import SpaceEventType
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.event_type_model import EventTypeModel

class SpaceEventTypeRepositoryImpl(SpaceEventTypeRepository):
    """Implementação do repositório para o relacionamento N:N entre Spaces e Event Types"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, space_event_type: SpaceEventType) -> SpaceEventType:
        """Criar um novo relacionamento entre espaço e tipo de evento"""
        # Verificar se o espaço existe
        space = self.db.query(SpaceModel).filter(SpaceModel.id == space_event_type.space_id).first()
        if not space:
            raise ValueError(f"Espaço com ID {space_event_type.space_id} não encontrado")
        
        # Verificar se o tipo de evento existe
        event_type = self.db.query(EventTypeModel).filter(EventTypeModel.id == space_event_type.event_type_id).first()
        if not event_type:
            raise ValueError(f"Tipo de evento com ID {space_event_type.event_type_id} não encontrado")
        
        # Criar o relacionamento
        db_space_event_type = SpaceEventTypeModel(
            space_id=space_event_type.space_id,
            event_type_id=space_event_type.event_type_id,
            tema=space_event_type.tema,
            descricao=space_event_type.descricao,
            link_divulgacao=space_event_type.link_divulgacao,
            banner=space_event_type.banner,
            data=space_event_type.data,
            horario=space_event_type.horario
        )
        
        self.db.add(db_space_event_type)
        self.db.commit()
        self.db.refresh(db_space_event_type)
        
        return self._to_entity(db_space_event_type)
    
    def get_by_id(self, space_event_type_id: int) -> Optional[SpaceEventType]:
        """Obter um relacionamento por ID"""
        relationship = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.id == space_event_type_id
        ).first()
        
        if not relationship:
            return None
        
        return self._to_entity(relationship)
    
    def get_by_space_id(self, space_id: int) -> List[SpaceEventType]:
        """Obter todos os tipos de eventos de um espaço"""
        relationships = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.space_id == space_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def get_by_event_type_id(self, event_type_id: int) -> List[SpaceEventType]:
        """Obter todos os espaços de um tipo de evento"""
        relationships = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.event_type_id == event_type_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def get_by_space_and_event_type(self, space_id: int, event_type_id: int) -> List[SpaceEventType]:
        """Obter relacionamentos específicos entre espaço e tipo de evento"""
        relationships = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.space_id == space_id,
            SpaceEventTypeModel.event_type_id == event_type_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def update(self, space_event_type_id: int, space_event_type: SpaceEventType) -> Optional[SpaceEventType]:
        """Atualizar um relacionamento"""
        db_relationship = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.id == space_event_type_id
        ).first()
        
        if not db_relationship:
            return None
        
        # Atualizar os campos
        if space_event_type.tema:
            db_relationship.tema = space_event_type.tema
        if space_event_type.descricao:
            db_relationship.descricao = space_event_type.descricao
        if space_event_type.link_divulgacao is not None:
            db_relationship.link_divulgacao = space_event_type.link_divulgacao
        if space_event_type.banner is not None:
            db_relationship.banner = space_event_type.banner
        if space_event_type.data:
            db_relationship.data = space_event_type.data
        if space_event_type.horario:
            db_relationship.horario = space_event_type.horario
        
        self.db.commit()
        self.db.refresh(db_relationship)
        
        return self._to_entity(db_relationship)
    
    def delete(self, space_event_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        relationship = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.id == space_event_type_id
        ).first()
        
        if not relationship:
            return False
        
        self.db.delete(relationship)
        self.db.commit()
        return True
    
    def delete_by_space_id(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        deleted_count = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.space_id == space_id
        ).delete()
        
        self.db.commit()
        return deleted_count > 0
    
    def delete_by_event_type_id(self, event_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de evento"""
        deleted_count = self.db.query(SpaceEventTypeModel).filter(
            SpaceEventTypeModel.event_type_id == event_type_id
        ).delete()
        
        self.db.commit()
        return deleted_count > 0
    
    def get_all(self) -> List[SpaceEventType]:
        """Obter todos os relacionamentos"""
        relationships = self.db.query(SpaceEventTypeModel).all()
        return [self._to_entity(rel) for rel in relationships]
    
    def _to_entity(self, model: SpaceEventTypeModel) -> SpaceEventType:
        """Converter modelo para entidade"""
        return SpaceEventType(
            id=model.id,
            space_id=model.space_id,
            event_type_id=model.event_type_id,
            tema=model.tema,
            descricao=model.descricao,
            link_divulgacao=model.link_divulgacao,
            banner=model.banner,
            data=model.data,
            horario=model.horario,
            created_at=model.created_at
        ) 