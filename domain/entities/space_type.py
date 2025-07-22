from datetime import datetime
from typing import Optional

class SpaceType:
    def __init__(
        self,
        tipo: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tipo = tipo
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 