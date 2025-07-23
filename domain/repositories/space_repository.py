from abc import ABC, abstractmethod
from typing import List, Optional, Union, TYPE_CHECKING
from domain.entities.space import Space

if TYPE_CHECKING:
    from infrastructure.database.models.space_model import SpaceModel

class SpaceRepository(ABC):
    @abstractmethod
    def create(self, space: Space) -> Space:
        pass

    @abstractmethod
    def get_by_id(self, space_id: int, include_relations: bool = False) -> Optional[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def get_by_space_type_id(self, space_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def get_by_event_type_id(self, event_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def get_by_festival_type_id(self, festival_type_id: int, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Space, "SpaceModel"]]:
        pass

    @abstractmethod
    def update(self, space: Space) -> Space:
        pass

    @abstractmethod
    def delete(self, space_id: int) -> bool:
        pass 