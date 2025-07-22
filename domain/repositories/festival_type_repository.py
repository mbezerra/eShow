from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.festival_type import FestivalType

class FestivalTypeRepository(ABC):
    @abstractmethod
    def create(self, festival_type: FestivalType) -> FestivalType:
        pass

    @abstractmethod
    def get_by_id(self, festival_type_id: int) -> Optional[FestivalType]:
        pass

    @abstractmethod
    def get_by_type(self, type: str) -> Optional[FestivalType]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[FestivalType]:
        pass

    @abstractmethod
    def update(self, festival_type: FestivalType) -> FestivalType:
        pass

    @abstractmethod
    def delete(self, festival_type_id: int) -> bool:
        pass 