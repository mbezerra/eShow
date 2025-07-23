from datetime import datetime
from typing import Optional, List, Any
from enum import Enum

class AcessoEnum(str, Enum):
    PUBLICO = "Público"
    PRIVADO = "Privado"

class PublicoEstimadoEnum(str, Enum):
    MENOS_50 = "<50"
    CINQUENTA_A_CEM = "51-100"
    CEM_A_QUINHENTOS = "101-500"
    QUINHENTOS_A_MIL = "501-1000"
    MIL_A_TRES_MIL = "1001-3000"
    TRES_MIL_A_CINCO_MIL = "3001-5000"
    CINCO_MIL_A_DEZ_MIL = "5001-10000"
    MAIS_DEZ_MIL = "> 10000"

class Space:
    def __init__(
        self,
        profile_id: int,
        space_type_id: int,
        acesso: AcessoEnum,
        dias_apresentacao: List[str],
        duracao_apresentacao: float,
        valor_hora: float,
        valor_couvert: float,
        requisitos_minimos: str,
        oferecimentos: str,
        estrutura_apresentacao: str,
        publico_estimado: PublicoEstimadoEnum,
        fotos_ambiente: List[str],
        instagram: Optional[str] = None,
        tiktok: Optional[str] = None,
        youtube: Optional[str] = None,
        facebook: Optional[str] = None,
        event_type_id: Optional[int] = None,
        festival_type_id: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.profile_id = profile_id
        self.space_type_id = space_type_id
        self.event_type_id = event_type_id
        self.festival_type_id = festival_type_id
        self.acesso = acesso
        self.dias_apresentacao = dias_apresentacao
        self.duracao_apresentacao = duracao_apresentacao
        self.valor_hora = valor_hora
        self.valor_couvert = valor_couvert
        self.requisitos_minimos = requisitos_minimos
        self.oferecimentos = oferecimentos
        self.estrutura_apresentacao = estrutura_apresentacao
        self.publico_estimado = publico_estimado
        self.fotos_ambiente = fotos_ambiente
        self.instagram = instagram
        self.tiktok = tiktok
        self.youtube = youtube
        self.facebook = facebook
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        
        # Relacionamentos (opcionais)
        self.profile = None
        self.space_type = None
        self.event_type = None
        self.festival_type = None 