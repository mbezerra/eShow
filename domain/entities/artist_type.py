from datetime import datetime
from typing import Optional
from enum import Enum

class ArtistTypeEnum(Enum):
    CANTOR_SOLO = "Cantor(a) solo"
    DUPLA = "Dupla"
    TRIO = "Trio"
    BANDA = "Banda"
    GRUPO = "Grupo"

class ArtistType:
    def __init__(
        self,
        tipo: ArtistTypeEnum,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tipo = tipo
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 