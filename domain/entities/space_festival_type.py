from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SpaceFestivalType:
    """Entidade de domínio para o relacionamento N:N entre Spaces e Festival Types"""
    space_id: int
    festival_type_id: int
    tema: str
    descricao: str
    data: datetime
    horario: str
    link_divulgacao: Optional[str] = None
    banner: Optional[str] = None  # Path local da imagem do banner
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.space_id <= 0:
            raise ValueError("ID do espaço deve ser maior que zero")
        if self.festival_type_id <= 0:
            raise ValueError("ID do tipo de festival deve ser maior que zero")
        if not self.tema or not self.tema.strip():
            raise ValueError("Tema é obrigatório")
        if not self.descricao or not self.descricao.strip():
            raise ValueError("Descrição é obrigatória")
        if not self.horario or not self.horario.strip():
            raise ValueError("Horário é obrigatório") 