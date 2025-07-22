from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.artist_musical_style import ArtistMusicalStyle

class ArtistMusicalStyleRepository(ABC):
    """Interface do repositório para o relacionamento N:N entre Artists e Musical Styles"""
    
    @abstractmethod
    def create(self, artist_musical_style: ArtistMusicalStyle) -> ArtistMusicalStyle:
        """Criar um novo relacionamento entre artista e estilo musical"""
        pass
    
    @abstractmethod
    def create_bulk(self, artist_id: int, musical_style_ids: List[int]) -> List[ArtistMusicalStyle]:
        """Criar múltiplos relacionamentos para um artista"""
        pass
    
    @abstractmethod
    def get_by_artist_id(self, artist_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os estilos musicais de um artista"""
        pass
    
    @abstractmethod
    def get_by_musical_style_id(self, musical_style_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os artistas de um estilo musical"""
        pass
    
    @abstractmethod
    def get_by_artist_and_style(self, artist_id: int, musical_style_id: int) -> Optional[ArtistMusicalStyle]:
        """Obter um relacionamento específico"""
        pass
    
    @abstractmethod
    def delete(self, artist_id: int, musical_style_id: int) -> bool:
        """Deletar um relacionamento específico"""
        pass
    
    @abstractmethod
    def delete_by_artist_id(self, artist_id: int) -> bool:
        """Deletar todos os relacionamentos de um artista"""
        pass
    
    @abstractmethod
    def delete_by_musical_style_id(self, musical_style_id: int) -> bool:
        """Deletar todos os relacionamentos de um estilo musical"""
        pass
    
    @abstractmethod
    def update_artist_styles(self, artist_id: int, musical_style_ids: List[int]) -> List[ArtistMusicalStyle]:
        """Atualizar todos os estilos musicais de um artista (substituir os existentes)"""
        pass 