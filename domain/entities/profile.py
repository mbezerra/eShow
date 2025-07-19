from datetime import datetime
from typing import Optional

class Profile:
    def __init__(
        self,
        role_id: int,
        full_name: str,
        artistic_name: str,
        bio: str,
        cep: str,
        logradouro: str,
        numero: str,
        cidade: str,
        uf: str,
        telefone_movel: str,
        complemento: Optional[str] = None,
        telefone_fixo: Optional[str] = None,
        whatsapp: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.role_id = role_id
        self.full_name = full_name
        self.artistic_name = artistic_name
        self.bio = bio
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade
        self.uf = uf
        self.telefone_fixo = telefone_fixo
        self.telefone_movel = telefone_movel
        self.whatsapp = whatsapp
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now() 