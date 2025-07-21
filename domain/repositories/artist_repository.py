from abc import ABC, abstractmethod
from typing import List, Optional, Union
from domain.entities.artist import Artist

class ArtistRepository(ABC):
    @abstractmethod
    def create(self, artist: Artist) -> Artist:
        """Criar um novo artista"""
        pass

    @abstractmethod
    def get_by_id(self, artist_id: int, include_relations: bool = False) -> Optional[Union[Artist, 'ArtistModel']]:
        """Obter artista por ID"""
        pass

    @abstractmethod
    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> Optional[Union[Artist, 'ArtistModel']]:
        """Obter artista por ID do profile"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, 'ArtistModel']]:
        """Listar todos os artistas"""
        pass

    @abstractmethod
    def get_by_artist_type(self, artist_type_id: int, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, 'ArtistModel']]:
        """Listar artistas por tipo"""
        pass

    @abstractmethod
    def update(self, artist: Artist) -> Artist:
        """Atualizar artista"""
        pass

    @abstractmethod
    def delete(self, artist_id: int) -> bool:
        """Deletar artista"""
        pass 