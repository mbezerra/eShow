from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories.space_festival_type_repository import SpaceFestivalTypeRepository
from domain.entities.space_festival_type import SpaceFestivalType, StatusFestivalType
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.festival_type_model import FestivalTypeModel

class SpaceFestivalTypeRepositoryImpl(SpaceFestivalTypeRepository):
    """Implementação do repositório para o relacionamento N:N entre Spaces e Festival Types"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, space_festival_type: SpaceFestivalType) -> SpaceFestivalType:
        """Criar um novo relacionamento entre espaço e tipo de festival"""
        # Verificar se o espaço existe
        space = self.db.query(SpaceModel).filter(SpaceModel.id == space_festival_type.space_id).first()
        if not space:
            raise ValueError(f"Espaço com ID {space_festival_type.space_id} não encontrado")
        
        # Verificar se o tipo de festival existe
        festival_type = self.db.query(FestivalTypeModel).filter(FestivalTypeModel.id == space_festival_type.festival_type_id).first()
        if not festival_type:
            raise ValueError(f"Tipo de festival com ID {space_festival_type.festival_type_id} não encontrado")
        
        # Criar o relacionamento
        db_space_festival_type = SpaceFestivalTypeModel(
            space_id=space_festival_type.space_id,
            festival_type_id=space_festival_type.festival_type_id,
            tema=space_festival_type.tema,
            descricao=space_festival_type.descricao,
            status=space_festival_type.status,
            link_divulgacao=space_festival_type.link_divulgacao,
            banner=space_festival_type.banner,
            data=space_festival_type.data,
            horario=space_festival_type.horario
        )
        
        self.db.add(db_space_festival_type)
        self.db.commit()
        self.db.refresh(db_space_festival_type)
        
        return self._to_entity(db_space_festival_type)
    
    def get_by_id(self, space_festival_type_id: int) -> Optional[SpaceFestivalType]:
        """Obter um relacionamento por ID"""
        relationship = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.id == space_festival_type_id
        ).first()
        
        if not relationship:
            return None
        
        return self._to_entity(relationship)
    
    def get_by_space_id(self, space_id: int) -> List[SpaceFestivalType]:
        """Obter todos os tipos de festivais de um espaço"""
        relationships = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.space_id == space_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def get_by_festival_type_id(self, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter todos os espaços de um tipo de festival"""
        relationships = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.festival_type_id == festival_type_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def get_by_space_and_festival_type(self, space_id: int, festival_type_id: int) -> List[SpaceFestivalType]:
        """Obter relacionamentos específicos entre espaço e tipo de festival"""
        relationships = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.space_id == space_id,
            SpaceFestivalTypeModel.festival_type_id == festival_type_id
        ).all()
        
        return [self._to_entity(rel) for rel in relationships]
    
    def update(self, space_festival_type_id: int, space_festival_type: SpaceFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar um relacionamento"""
        db_relationship = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.id == space_festival_type_id
        ).first()
        
        if not db_relationship:
            return None
        
        # Atualizar os campos
        if space_festival_type.tema:
            db_relationship.tema = space_festival_type.tema
        if space_festival_type.descricao:
            db_relationship.descricao = space_festival_type.descricao
        if space_festival_type.status:
            db_relationship.status = space_festival_type.status
        if space_festival_type.link_divulgacao is not None:
            db_relationship.link_divulgacao = space_festival_type.link_divulgacao
        if space_festival_type.banner is not None:
            db_relationship.banner = space_festival_type.banner
        if space_festival_type.data:
            db_relationship.data = space_festival_type.data
        if space_festival_type.horario:
            db_relationship.horario = space_festival_type.horario
        
        self.db.commit()
        self.db.refresh(db_relationship)
        
        return self._to_entity(db_relationship)
    
    def update_status(self, space_festival_type_id: int, status: StatusFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar apenas o status de um relacionamento"""
        db_relationship = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.id == space_festival_type_id
        ).first()
        
        if not db_relationship:
            return None
        
        db_relationship.status = status
        self.db.commit()
        self.db.refresh(db_relationship)
        
        return self._to_entity(db_relationship)
    
    def delete(self, space_festival_type_id: int) -> bool:
        """Deletar um relacionamento específico"""
        relationship = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.id == space_festival_type_id
        ).first()
        
        if not relationship:
            return False
        
        self.db.delete(relationship)
        self.db.commit()
        return True
    
    def delete_by_space_id(self, space_id: int) -> bool:
        """Deletar todos os relacionamentos de um espaço"""
        deleted_count = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.space_id == space_id
        ).delete()
        
        self.db.commit()
        return deleted_count > 0
    
    def delete_by_festival_type_id(self, festival_type_id: int) -> bool:
        """Deletar todos os relacionamentos de um tipo de festival"""
        deleted_count = self.db.query(SpaceFestivalTypeModel).filter(
            SpaceFestivalTypeModel.festival_type_id == festival_type_id
        ).delete()
        
        self.db.commit()
        return deleted_count > 0
    
    def get_all(self) -> List[SpaceFestivalType]:
        """Obter todos os relacionamentos"""
        relationships = self.db.query(SpaceFestivalTypeModel).all()
        return [self._to_entity(rel) for rel in relationships]
    
    def _to_entity(self, model: SpaceFestivalTypeModel) -> SpaceFestivalType:
        """Converter modelo para entidade"""
        return SpaceFestivalType(
            id=model.id,
            space_id=model.space_id,
            festival_type_id=model.festival_type_id,
            tema=model.tema,
            descricao=model.descricao,
            status=model.status,
            link_divulgacao=model.link_divulgacao,
            banner=model.banner,
            data=model.data,
            horario=model.horario,
            created_at=model.created_at
        ) 