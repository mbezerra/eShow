from datetime import datetime
from typing import Optional

class EventType:
    def __init__(
        self,
        type: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.type = type
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 