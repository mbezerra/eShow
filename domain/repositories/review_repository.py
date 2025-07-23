from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
from datetime import datetime
from domain.entities.review import Review

class ReviewRepository(ABC):
    """Interface do repositório para avaliações/reviews"""
    
    @abstractmethod
    def create(self, review: Review) -> Review:
        """Criar uma nova avaliação"""
        pass
    
    @abstractmethod
    def get_by_id(self, review_id: int, include_relations: bool = False) -> Optional[Union[Review, Any]]:
        """Obter uma avaliação por ID"""
        pass
    
    @abstractmethod
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um profile"""
        pass
    
    @abstractmethod
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um space-event type"""
        pass
    
    @abstractmethod
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações de um space-festival type"""
        pass
    
    @abstractmethod
    def get_by_nota(self, nota: int, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações com uma nota específica"""
        pass
    
    @abstractmethod
    def get_by_date_range(self, data_inicio: datetime, data_fim: datetime, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter avaliações em um período"""
        pass
    
    @abstractmethod
    def update(self, review_id: int, review: Review) -> Optional[Review]:
        """Atualizar uma avaliação"""
        pass
    
    @abstractmethod
    def delete(self, review_id: int) -> bool:
        """Deletar uma avaliação"""
        pass
    
    @abstractmethod
    def get_all(self, include_relations: bool = False) -> List[Union[Review, Any]]:
        """Obter todas as avaliações"""
        pass
    
    @abstractmethod
    def get_average_rating_by_profile(self, profile_id: int) -> Optional[float]:
        """Obter a média de avaliações de um profile"""
        pass 