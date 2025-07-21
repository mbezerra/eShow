from datetime import datetime
from typing import Optional

class MusicalStyle:
    def __init__(
        self,
        estyle: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.estyle = estyle
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 