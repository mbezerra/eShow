from typing import List, Optional, Union, Any
from datetime import datetime
from sqlalchemy.orm import Session
from domain.entities.review import Review
from domain.repositories.review_repository import ReviewRepository
from infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    """Serviço de aplicação para avaliações/reviews"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository: ReviewRepository = ReviewRepositoryImpl(db)
    
    def create_review(self, review_data: ReviewCreate) -> Review:
        """Criar uma nova avaliação"""
        review = Review(
            profile_id=review_data.profile_id,
            space_event_type_id=review_data.space_event_type_id,
            space_festival_type_id=review_data.space_festival_type_id,
            data_hora=review_data.data_hora,
            nota=review_data.nota,
            depoimento=review_data.depoimento
        )
        
        return self.repository.create(review)
    
    def get_review_by_id(self, review_id: int, include_relations: bool = False) -> Optional[Union[Review, Any]]:
        """Obter uma avaliação por ID"""
        return self.repository.get_by_id(review_id, include_relations)
    
    def get_reviews_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um profile"""
        return self.repository.get_by_profile_id(profile_id, include_relations)
    
    def get_reviews_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um space-event type"""
        return self.repository.get_by_space_event_type_id(space_event_type_id, include_relations)
    
    def get_reviews_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um space-festival type"""
        return self.repository.get_by_space_festival_type_id(space_festival_type_id, include_relations)
    
    def get_reviews_by_nota(self, nota: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações com uma nota específica"""
        return self.repository.get_by_nota(nota, include_relations)
    
    def get_reviews_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter avaliações em um período"""
        return self.repository.get_by_date_range(data_inicio, data_fim, include_relations)
    
    def update_review(self, review_id: int, review_data: ReviewUpdate) -> Optional[Review]:
        """Atualizar uma avaliação"""
        # Primeiro verificar se a avaliação existe
        existing_review = self.repository.get_by_id(review_id)
        if not existing_review:
            return None
        
        # Criar entidade com os dados atualizados
        updated_review = Review(
            profile_id=existing_review.profile_id,  # Profile não pode ser alterado
            space_event_type_id=review_data.space_event_type_id if review_data.space_event_type_id is not None else existing_review.space_event_type_id,
            space_festival_type_id=review_data.space_festival_type_id if review_data.space_festival_type_id is not None else existing_review.space_festival_type_id,
            data_hora=review_data.data_hora if review_data.data_hora is not None else existing_review.data_hora,
            nota=review_data.nota if review_data.nota is not None else existing_review.nota,
            depoimento=review_data.depoimento if review_data.depoimento is not None else existing_review.depoimento
        )
        
        return self.repository.update(review_id, updated_review)
    
    def delete_review(self, review_id: int) -> bool:
        """Deletar uma avaliação"""
        return self.repository.delete(review_id)
    
    def get_all_reviews(self, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações"""
        return self.repository.get_all(include_relations)
    
    def get_average_rating_by_profile(self, profile_id: int) -> dict:
        """Obter a média de avaliações de um profile"""
        average = self.repository.get_average_rating_by_profile(profile_id)
        reviews = self.repository.get_by_profile_id(profile_id)
        
        return {
            "profile_id": profile_id,
            "average_rating": average,
            "total_reviews": len(reviews)
        }
    
    def validate_business_rules(self, review_data: ReviewCreate) -> List[str]:
        """Validar regras de negócio específicas"""
        errors = []
        
        # Verificar se apenas um tipo de relacionamento foi especificado
        relationships = [review_data.space_event_type_id, review_data.space_festival_type_id]
        defined_relationships = [rel for rel in relationships if rel is not None]
        
        if len(defined_relationships) > 1:
            errors.append("Apenas um tipo de relacionamento pode ser especificado por review")
        
        # Verificar se pelo menos um relacionamento foi especificado
        if len(defined_relationships) == 0:
            errors.append("Pelo menos um relacionamento deve ser especificado (space_event_type_id ou space_festival_type_id)")
        
        return errors 