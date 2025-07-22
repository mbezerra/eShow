from typing import List, Optional
from domain.repositories.artist_musical_style_repository import ArtistMusicalStyleRepository
from domain.entities.artist_musical_style import ArtistMusicalStyle
from app.schemas.artist_musical_style import ArtistMusicalStyleCreate, ArtistMusicalStyleBulkCreate

class ArtistMusicalStyleService:
    """Serviço de aplicação para o relacionamento N:N entre Artists e Musical Styles"""
    
    def __init__(self, artist_musical_style_repository: ArtistMusicalStyleRepository):
        self.artist_musical_style_repository = artist_musical_style_repository
    
    def create_artist_musical_style(self, artist_musical_style_data: ArtistMusicalStyleCreate) -> ArtistMusicalStyle:
        """Criar um novo relacionamento entre artista e estilo musical"""
        artist_musical_style = ArtistMusicalStyle(
            artist_id=artist_musical_style_data.artist_id,
            musical_style_id=artist_musical_style_data.musical_style_id
        )
        
        return self.artist_musical_style_repository.create(artist_musical_style)
    
    def create_bulk_artist_musical_styles(self, bulk_data: ArtistMusicalStyleBulkCreate) -> List[ArtistMusicalStyle]:
        """Criar múltiplos relacionamentos para um artista"""
        return self.artist_musical_style_repository.create_bulk(
            bulk_data.artist_id, 
            bulk_data.musical_style_ids
        )
    
    def get_musical_styles_by_artist(self, artist_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os estilos musicais de um artista"""
        return self.artist_musical_style_repository.get_by_artist_id(artist_id)
    
    def get_artists_by_musical_style(self, musical_style_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os artistas de um estilo musical"""
        return self.artist_musical_style_repository.get_by_musical_style_id(musical_style_id)
    
    def get_artist_musical_style(self, artist_id: int, musical_style_id: int) -> Optional[ArtistMusicalStyle]:
        """Obter um relacionamento específico"""
        return self.artist_musical_style_repository.get_by_artist_and_style(artist_id, musical_style_id)
    
    def delete_artist_musical_style(self, artist_id: int, musical_style_id: int) -> bool:
        """Deletar um relacionamento específico"""
        return self.artist_musical_style_repository.delete(artist_id, musical_style_id)
    
    def delete_all_artist_musical_styles(self, artist_id: int) -> bool:
        """Deletar todos os relacionamentos de um artista"""
        return self.artist_musical_style_repository.delete_by_artist_id(artist_id)
    
    def delete_all_musical_style_artists(self, musical_style_id: int) -> bool:
        """Deletar todos os relacionamentos de um estilo musical"""
        return self.artist_musical_style_repository.delete_by_musical_style_id(musical_style_id)
    
    def update_artist_musical_styles(self, artist_id: int, musical_style_ids: List[int]) -> List[ArtistMusicalStyle]:
        """Atualizar todos os estilos musicais de um artista (substituir os existentes)"""
        return self.artist_musical_style_repository.update_artist_styles(artist_id, musical_style_ids) 