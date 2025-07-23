from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from domain.repositories.review_repository import ReviewRepository
from domain.entities.review import Review
from infrastructure.database.models.review_model import ReviewModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel

class ReviewRepositoryImpl(ReviewRepository):
    """Implementação do repositório para avaliações/reviews"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _configure_relations(self, query, include_relations: bool = False):
        """Configurar relacionamentos para a query"""
        if include_relations:
            query = query.options(
                joinedload(ReviewModel.profile),
                joinedload(ReviewModel.space_event_type),
                joinedload(ReviewModel.space_festival_type)
            )
        return query
    
    def create(self, review: Review) -> Review:
        """Criar uma nova avaliação"""
        # Verificar se o profile existe
        profile = self.db.query(ProfileModel).filter(ProfileModel.id == review.profile_id).first()
        if not profile:
            raise ValueError(f"Profile com ID {review.profile_id} não encontrado")
        
        # Verificar se os relacionamentos existem quando especificados
        if review.space_event_type_id:
            space_event_type = self.db.query(SpaceEventTypeModel).filter(SpaceEventTypeModel.id == review.space_event_type_id).first()
            if not space_event_type:
                raise ValueError(f"Space-Event Type com ID {review.space_event_type_id} não encontrado")
        
        if review.space_festival_type_id:
            space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(SpaceFestivalTypeModel.id == review.space_festival_type_id).first()
            if not space_festival_type:
                raise ValueError(f"Space-Festival Type com ID {review.space_festival_type_id} não encontrado")
        
        # Criar a avaliação
        db_review = ReviewModel(
            profile_id=review.profile_id,
            space_event_type_id=review.space_event_type_id,
            space_festival_type_id=review.space_festival_type_id,
            data_hora=review.data_hora,
            nota=review.nota,
            depoimento=review.depoimento
        )
        
        self.db.add(db_review)
        self.db.commit()
        self.db.refresh(db_review)
        
        return self._to_entity(db_review)
    
    def get_by_id(self, review_id: int, include_relations: bool = False) -> Optional[Union[Review, ReviewModel]]:
        """Obter uma avaliação por ID"""
        query = self.db.query(ReviewModel).filter(ReviewModel.id == review_id)
        query = self._configure_relations(query, include_relations)
        review = query.first()
        
        if not review:
            return None
        
        if include_relations:
            return review  # Retorna o modelo com relacionamentos carregados
        return self._to_entity(review)
    
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter todas as avaliações de um profile"""
        query = self.db.query(ReviewModel).filter(ReviewModel.profile_id == profile_id)
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter todas as avaliações de um space-event type"""
        query = self.db.query(ReviewModel).filter(ReviewModel.space_event_type_id == space_event_type_id)
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter todas as avaliações de um space-festival type"""
        query = self.db.query(ReviewModel).filter(ReviewModel.space_festival_type_id == space_festival_type_id)
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def get_by_nota(self, nota: int, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter todas as avaliações com uma nota específica"""
        query = self.db.query(ReviewModel).filter(ReviewModel.nota == nota)
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def get_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter avaliações em um período"""
        query = self.db.query(ReviewModel).filter(
            ReviewModel.data_hora >= data_inicio,
            ReviewModel.data_hora <= data_fim
        )
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def update(self, review_id: int, review: Review) -> Optional[Review]:
        """Atualizar uma avaliação"""
        db_review = self.db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        
        if not db_review:
            return None
        
        # Verificar relacionamentos se foram alterados
        if review.space_event_type_id and review.space_event_type_id != db_review.space_event_type_id:
            space_event_type = self.db.query(SpaceEventTypeModel).filter(SpaceEventTypeModel.id == review.space_event_type_id).first()
            if not space_event_type:
                raise ValueError(f"Space-Event Type com ID {review.space_event_type_id} não encontrado")
        
        if review.space_festival_type_id and review.space_festival_type_id != db_review.space_festival_type_id:
            space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(SpaceFestivalTypeModel.id == review.space_festival_type_id).first()
            if not space_festival_type:
                raise ValueError(f"Space-Festival Type com ID {review.space_festival_type_id} não encontrado")
        
        # Atualizar os campos (profile_id não pode ser alterado)
        if review.data_hora:
            db_review.data_hora = review.data_hora
        if review.nota:
            db_review.nota = review.nota
        if review.depoimento:
            db_review.depoimento = review.depoimento
        if review.space_event_type_id is not None:
            db_review.space_event_type_id = review.space_event_type_id
        if review.space_festival_type_id is not None:
            db_review.space_festival_type_id = review.space_festival_type_id
        
        self.db.commit()
        self.db.refresh(db_review)
        
        return self._to_entity(db_review)
    
    def delete(self, review_id: int) -> bool:
        """Deletar uma avaliação"""
        review = self.db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        
        if not review:
            return False
        
        self.db.delete(review)
        self.db.commit()
        return True
    
    def get_all(self, include_relations: bool = False) -> List[Union[Review, ReviewModel]]:
        """Obter todas as avaliações"""
        query = self.db.query(ReviewModel)
        query = self._configure_relations(query, include_relations)
        reviews = query.all()
        
        if include_relations:
            return reviews  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(review) for review in reviews]
    
    def get_average_rating_by_profile(self, profile_id: int) -> Optional[float]:
        """Obter a média de avaliações de um profile"""
        result = self.db.query(func.avg(ReviewModel.nota)).filter(ReviewModel.profile_id == profile_id).scalar()
        
        if result is None:
            return None
        
        return round(float(result), 2)
    
    def _to_entity(self, model: ReviewModel) -> Review:
        """Converter modelo para entidade"""
        return Review(
            id=model.id,
            profile_id=model.profile_id,
            space_event_type_id=model.space_event_type_id,
            space_festival_type_id=model.space_festival_type_id,
            data_hora=model.data_hora,
            nota=model.nota,
            depoimento=model.depoimento,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 