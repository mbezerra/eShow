from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.artist_type import ArtistType, ArtistTypeEnum

class ArtistTypeRepository(ABC):
    @abstractmethod
    def create(self, artist_type: ArtistType) -> ArtistType:
        pass
    
    @abstractmethod
    def get_by_id(self, artist_type_id: int) -> Optional[ArtistType]:
        pass
    
    @abstractmethod
    def get_by_tipo(self, tipo: ArtistTypeEnum) -> Optional[ArtistType]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ArtistType]:
        pass
    
    @abstractmethod
    def update(self, artist_type: ArtistType) -> ArtistType:
        pass
    
    @abstractmethod
    def delete(self, artist_type_id: int) -> bool:
        pass 