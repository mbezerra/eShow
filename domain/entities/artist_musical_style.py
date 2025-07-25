from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ArtistMusicalStyle:
    """Entidade de domínio para o relacionamento N:N entre Artists e Musical Styles"""
    artist_id: int
    musical_style_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.artist_id <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        if self.musical_style_id <= 0:
            raise ValueError("ID do estilo musical deve ser maior que zero") 