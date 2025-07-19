from datetime import datetime
from typing import Optional
from enum import Enum

class RoleType(Enum):
    ADMIN = "Admin"
    ARTISTA = "Artista"
    ESPACO = "Espaço"

class Role:
    def __init__(
        self,
        role: RoleType,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.role = role
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 