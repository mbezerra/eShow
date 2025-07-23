from typing import List, Optional, Union
from sqlalchemy.orm import Session, joinedload
from domain.entities.space import Space
from domain.repositories.space_repository import SpaceRepository
from infrastructure.database.models.space_model import SpaceModel

class SpaceRepositoryImpl(SpaceRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, space: Space) -> Space:
        db_space = SpaceModel(
            profile_id=space.profile_id,
            space_type_id=space.space_type_id,
            event_type_id=space.event_type_id,
            festival_type_id=space.festival_type_id,
            acesso=space.acesso,
            dias_apresentacao=space.dias_apresentacao,
            duracao_apresentacao=space.duracao_apresentacao,
            valor_hora=space.valor_hora,
            valor_couvert=space.valor_couvert,
            requisitos_minimos=space.requisitos_minimos,
            oferecimentos=space.oferecimentos,
            estrutura_apresentacao=space.estrutura_apresentacao,
            publico_estimado=space.publico_estimado,
            fotos_ambiente=space.fotos_ambiente,
            instagram=space.instagram,
            tiktok=space.tiktok,
            youtube=space.youtube,
            facebook=space.facebook
        )
        self.db.add(db_space)
        self.db.commit()
        self.db.refresh(db_space)
        return self._to_entity(db_space)

    def get_by_id(self, space_id: int, include_relations: bool = False) -> Optional[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_space = query.filter(SpaceModel.id == space_id).first()
        if db_space is None:
            return None
        
        # Se include_relations=True, retornar o modelo do banco diretamente
        if include_relations:
            return db_space
        else:
            return self._to_entity(db_space)

    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel).filter(SpaceModel.profile_id == profile_id)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_spaces = query.all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_spaces
        else:
            return [self._to_entity(db_space) for db_space in db_spaces]

    def get_by_space_type_id(self, space_type_id: int, include_relations: bool = False) -> List[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel).filter(SpaceModel.space_type_id == space_type_id)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_spaces = query.all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_spaces
        else:
            return [self._to_entity(db_space) for db_space in db_spaces]

    def get_by_event_type_id(self, event_type_id: int, include_relations: bool = False) -> List[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel).filter(SpaceModel.event_type_id == event_type_id)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_spaces = query.all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_spaces
        else:
            return [self._to_entity(db_space) for db_space in db_spaces]

    def get_by_festival_type_id(self, festival_type_id: int, include_relations: bool = False) -> List[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel).filter(SpaceModel.festival_type_id == festival_type_id)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_spaces = query.all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_spaces
        else:
            return [self._to_entity(db_space) for db_space in db_spaces]

    def get_all(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Space, SpaceModel]]:
        query = self.db.query(SpaceModel)
        
        if include_relations:
            query = query.options(
                joinedload(SpaceModel.profile),
                joinedload(SpaceModel.space_type),
                joinedload(SpaceModel.event_type),
                joinedload(SpaceModel.festival_type)
            )
        
        db_spaces = query.offset(skip).limit(limit).all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_spaces
        else:
            return [self._to_entity(db_space) for db_space in db_spaces]

    def update(self, space: Space) -> Space:
        db_space = self.db.query(SpaceModel).filter(SpaceModel.id == space.id).first()
        if db_space is None:
            raise ValueError(f"Space with id {space.id} not found")

        db_space.profile_id = space.profile_id
        db_space.space_type_id = space.space_type_id
        db_space.event_type_id = space.event_type_id
        db_space.festival_type_id = space.festival_type_id
        db_space.acesso = space.acesso
        db_space.dias_apresentacao = space.dias_apresentacao
        db_space.duracao_apresentacao = space.duracao_apresentacao
        db_space.valor_hora = space.valor_hora
        db_space.valor_couvert = space.valor_couvert
        db_space.requisitos_minimos = space.requisitos_minimos
        db_space.oferecimentos = space.oferecimentos
        db_space.estrutura_apresentacao = space.estrutura_apresentacao
        db_space.publico_estimado = space.publico_estimado
        db_space.fotos_ambiente = space.fotos_ambiente
        db_space.instagram = space.instagram
        db_space.tiktok = space.tiktok
        db_space.youtube = space.youtube
        db_space.facebook = space.facebook

        self.db.commit()
        self.db.refresh(db_space)
        return self._to_entity(db_space)

    def delete(self, space_id: int) -> bool:
        db_space = self.db.query(SpaceModel).filter(SpaceModel.id == space_id).first()
        if db_space is None:
            return False

        self.db.delete(db_space)
        self.db.commit()
        return True

    def _to_entity(self, db_space: SpaceModel) -> Space:
        space = Space(
            id=db_space.id,
            profile_id=db_space.profile_id,
            space_type_id=db_space.space_type_id,
            event_type_id=db_space.event_type_id,
            festival_type_id=db_space.festival_type_id,
            acesso=db_space.acesso,
            dias_apresentacao=db_space.dias_apresentacao,
            duracao_apresentacao=db_space.duracao_apresentacao,
            valor_hora=db_space.valor_hora,
            valor_couvert=db_space.valor_couvert,
            requisitos_minimos=db_space.requisitos_minimos,
            oferecimentos=db_space.oferecimentos,
            estrutura_apresentacao=db_space.estrutura_apresentacao,
            publico_estimado=db_space.publico_estimado,
            fotos_ambiente=db_space.fotos_ambiente,
            instagram=db_space.instagram,
            tiktok=db_space.tiktok,
            youtube=db_space.youtube,
            facebook=db_space.facebook,
            created_at=db_space.created_at,
            updated_at=db_space.updated_at
        )
        
        # Não adicionar relacionamentos na entidade - eles só são incluídos quando retornamos o modelo do banco
            
        return space 