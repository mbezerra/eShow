from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Booking:
    """Entidade de domínio para agendamentos/reservas"""
    profile_id: int
    data_inicio: datetime
    horario_inicio: str
    data_fim: datetime
    horario_fim: str
    space_id: Optional[int] = None  # Para agendamento de artista
    artist_id: Optional[int] = None  # Para agendamento de espaço
    space_event_type_id: Optional[int] = None  # Para eventos
    space_festival_type_id: Optional[int] = None  # Para festivais
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.profile_id <= 0:
            raise ValueError("ID do profile deve ser maior que zero")
        
        if not self.horario_inicio or not self.horario_inicio.strip():
            raise ValueError("Horário de início é obrigatório")
        
        if not self.horario_fim or not self.horario_fim.strip():
            raise ValueError("Horário de fim é obrigatório")
        
        if self.data_fim < self.data_inicio:
            raise ValueError("Data de fim deve ser posterior à data de início")
        
        if self.data_fim == self.data_inicio and self.horario_fim <= self.horario_inicio:
            raise ValueError("Horário de fim deve ser posterior ao horário de início quando no mesmo dia")
        
        # Validar que apenas um tipo de relacionamento está definido
        related_fields = [self.space_id, self.artist_id, self.space_event_type_id, self.space_festival_type_id]
        defined_fields = [field for field in related_fields if field is not None]
        
        if len(defined_fields) == 0:
            raise ValueError("Pelo menos um relacionamento deve ser especificado (space, artist, space_event_type ou space_festival_type)")
        
        if len(defined_fields) > 1:
            raise ValueError("Apenas um tipo de relacionamento pode ser especificado por booking")
        
        # Validar IDs positivos quando definidos
        if self.space_id is not None and self.space_id <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        
        if self.artist_id is not None and self.artist_id <= 0:
            raise ValueError("ID do artista deve ser maior que zero")
        
        if self.space_event_type_id is not None and self.space_event_type_id <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        
        if self.space_festival_type_id is not None and self.space_festival_type_id <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero") 