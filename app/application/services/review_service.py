from typing import List, Optional, Union, Any
from datetime import datetime
from sqlalchemy.orm import Session
from domain.entities.review import Review
from domain.repositories.review_repository import ReviewRepository
from infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl
from infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    """Serviço de aplicação para avaliações/reviews"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository: ReviewRepository = ReviewRepositoryImpl(db)
        self.profile_repository = ProfileRepositoryImpl(db)
    
    def create_review(self, review_data: ReviewCreate) -> Review:
        """Criar uma nova avaliação"""
        # Validar regras de negócio antes de criar
        errors = self.validate_business_rules(review_data)
        if errors:
            raise ValueError("; ".join(errors))
        
        review = Review(
            profile_id=review_data.profile_id,
            space_event_type_id=review_data.space_event_type_id,
            space_festival_type_id=review_data.space_festival_type_id,
            data_hora=review_data.data_hora,
            nota=review_data.nota,
            depoimento=review_data.depoimento
        )
        
        return self.repository.create(review)
    
    def create_review_with_profile(self, review_data: ReviewCreate, profile_id: int) -> Review:
        """Criar uma nova avaliação com profile_id específico"""
        # Validar regras de negócio antes de criar
        errors = self.validate_business_rules_with_profile(review_data, profile_id)
        if errors:
            raise ValueError("; ".join(errors))
        
        review = Review(
            profile_id=profile_id,
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
        
        # Validar regras de role para reviews
        role_errors = self._validate_role_rules(review_data)
        errors.extend(role_errors)
        
        return errors
    
    def validate_business_rules_with_profile(self, review_data: ReviewCreate, profile_id: int) -> List[str]:
        """Validar regras de negócio específicas com profile_id fornecido"""
        errors = []
        
        # Verificar se apenas um tipo de relacionamento foi especificado
        relationships = [review_data.space_event_type_id, review_data.space_festival_type_id]
        defined_relationships = [rel for rel in relationships if rel is not None]
        
        if len(defined_relationships) > 1:
            errors.append("Apenas um tipo de relacionamento pode ser especificado por review")
        
        # Verificar se pelo menos um relacionamento foi especificado
        if len(defined_relationships) == 0:
            errors.append("Pelo menos um relacionamento deve ser especificado (space_event_type_id ou space_festival_type_id)")
        
        # Validar regras de role para reviews
        role_errors = self._validate_role_rules_with_profile(review_data, profile_id)
        errors.extend(role_errors)
        
        return errors
    
    def _validate_role_rules(self, review_data: ReviewCreate) -> List[str]:
        """Validar regras específicas de role para reviews"""
        errors = []
        
        try:
            # Obter o profile que está fazendo a avaliação
            profile = self.profile_repository.get_by_id(review_data.profile_id)
            if not profile:
                errors.append(f"Profile com ID {review_data.profile_id} não encontrado")
                return errors
            
            # Regra 1: Usuários com role_id = 1 (ADMIN) NUNCA avaliam ou são avaliados
            if profile.role_id == 1:
                errors.append("Usuários com role ADMIN (role_id = 1) não podem fazer avaliações. Seu papel é apenas administrativo.")
                return errors
            
            # Regra 2: Usuários com role_id = 2 (ARTISTA) SEMPRE avaliam role_id = 3 (ESPAÇO)
            if profile.role_id == 2:
                # Verificar se está avaliando um espaço (role_id = 3)
                # Para isso, precisamos verificar o space_event_type ou space_festival_type
                # e obter o profile do espaço através do relacionamento
                space_profile = self._get_space_profile_from_review(review_data)
                if space_profile and space_profile.role_id != 3:
                    errors.append("Usuários com role ARTISTA (role_id = 2) só podem avaliar usuários com role ESPAÇO (role_id = 3)")
            
            # Regra 3: Usuários com role_id = 3 (ESPAÇO) SEMPRE avaliam role_id = 2 (ARTISTA)
            elif profile.role_id == 3:
                # Verificar se está avaliando um artista (role_id = 2)
                artist_profile = self._get_artist_profile_from_review(review_data)
                if artist_profile and artist_profile.role_id != 2:
                    errors.append("Usuários com role ESPAÇO (role_id = 3) só podem avaliar usuários com role ARTISTA (role_id = 2)")
            
            # Se chegou aqui, o role_id não é válido (deveria ser 1, 2 ou 3)
            else:
                errors.append(f"Role_id {profile.role_id} não é válido para fazer avaliações")
                
        except Exception as e:
            errors.append(f"Erro ao validar regras de role: {str(e)}")
        
        return errors
    
    def _validate_role_rules_with_profile(self, review_data: ReviewCreate, profile_id: int) -> List[str]:
        """Validar regras específicas de role para reviews com profile_id fornecido"""
        errors = []
        
        try:
            # Obter o profile que está fazendo a avaliação
            profile = self.profile_repository.get_by_id(profile_id)
            if not profile:
                errors.append(f"Profile com ID {profile_id} não encontrado")
                return errors
            
            # Regra 1: Usuários com role_id = 1 (ADMIN) NUNCA avaliam ou são avaliados
            if profile.role_id == 1:
                error_msg = "Usuários com role ADMIN (role_id = 1) não podem fazer avaliações. Seu papel é apenas administrativo."
                errors.append(error_msg)
                return errors
            
            # Regra 2: Usuários com role_id = 2 (ARTISTA) SEMPRE avaliam role_id = 3 (ESPAÇO)
            if profile.role_id == 2:
                # Verificar se está avaliando um espaço (role_id = 3)
                # Para isso, precisamos verificar o space_event_type ou space_festival_type
                # e obter o profile do espaço através do relacionamento
                space_profile = self._get_space_profile_from_review(review_data)
                if space_profile and space_profile.role_id != 3:
                    errors.append("Usuários com role ARTISTA (role_id = 2) só podem avaliar usuários com role ESPAÇO (role_id = 3)")
            
            # Regra 3: Usuários com role_id = 3 (ESPAÇO) SEMPRE avaliam role_id = 2 (ARTISTA)
            elif profile.role_id == 3:
                # Verificar se está avaliando um artista (role_id = 2)
                artist_profile = self._get_artist_profile_from_review(review_data)
                if artist_profile and artist_profile.role_id != 2:
                    errors.append("Usuários com role ESPAÇO (role_id = 3) só podem avaliar usuários com role ARTISTA (role_id = 2)")
            
            # Se chegou aqui, o role_id não é válido (deveria ser 1, 2 ou 3)
            else:
                errors.append(f"Role_id {profile.role_id} não é válido para fazer avaliações")
                
        except Exception as e:
            errors.append(f"Erro ao validar regras de role: {str(e)}")
        
        return errors
    
    def _get_space_profile_from_review(self, review_data: ReviewCreate) -> Optional[Any]:
        """Obter o profile do espaço a partir do review_data"""
        try:
            if review_data.space_event_type_id:
                # Buscar o space_event_type e obter o profile do espaço
                from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
                from infrastructure.database.models.space_model import SpaceModel
                
                space_event_type = self.db.query(SpaceEventTypeModel).filter(
                    SpaceEventTypeModel.id == review_data.space_event_type_id
                ).first()
                
                if space_event_type:
                    space = self.db.query(SpaceModel).filter(
                        SpaceModel.id == space_event_type.space_id
                    ).first()
                    
                    if space:
                        return self.profile_repository.get_by_id(space.profile_id)
            
            elif review_data.space_festival_type_id:
                # Buscar o space_festival_type e obter o profile do espaço
                from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel
                from infrastructure.database.models.space_model import SpaceModel
                
                space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(
                    SpaceFestivalTypeModel.id == review_data.space_festival_type_id
                ).first()
                
                if space_festival_type:
                    space = self.db.query(SpaceModel).filter(
                        SpaceModel.id == space_festival_type.space_id
                    ).first()
                    
                    if space:
                        return self.profile_repository.get_by_id(space.profile_id)
            
            return None
            
        except Exception:
            return None
    
    def _get_artist_profile_from_review(self, review_data: ReviewCreate) -> Optional[Any]:
        """Obter o profile do artista a partir do review_data"""
        try:
            if review_data.space_event_type_id:
                # Para space_event_type, o artista seria quem está sendo avaliado
                # Isso seria mais complexo e pode precisar de ajuste na estrutura
                # Por enquanto, vamos assumir que o profile_id no review é do artista
                return self.profile_repository.get_by_id(review_data.profile_id)
            
            elif review_data.space_festival_type_id:
                # Similar ao space_event_type
                return self.profile_repository.get_by_id(review_data.profile_id)
            
            return None
            
        except Exception:
            return None 