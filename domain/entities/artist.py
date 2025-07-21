from datetime import datetime
from typing import Optional, List

class Artist:
    def __init__(
        self,
        profile_id: int,
        artist_type_id: int,
        dias_apresentacao: List[str],
        raio_atuacao: float,
        duracao_apresentacao: float,
        valor_hora: float,
        valor_couvert: float,
        requisitos_minimos: str,
        instagram: Optional[str] = None,
        tiktok: Optional[str] = None,
        youtube: Optional[str] = None,
        facebook: Optional[str] = None,
        soundcloud: Optional[str] = None,
        bandcamp: Optional[str] = None,
        spotify: Optional[str] = None,
        deezer: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.profile_id = profile_id
        self.artist_type_id = artist_type_id
        self.dias_apresentacao = dias_apresentacao
        self.raio_atuacao = raio_atuacao
        self.duracao_apresentacao = duracao_apresentacao
        self.valor_hora = valor_hora
        self.valor_couvert = valor_couvert
        self.requisitos_minimos = requisitos_minimos
        self.instagram = instagram
        self.tiktok = tiktok
        self.youtube = youtube
        self.facebook = facebook
        self.soundcloud = soundcloud
        self.bandcamp = bandcamp
        self.spotify = spotify
        self.deezer = deezer
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self):
        return f"<Artist(id={self.id}, profile_id={self.profile_id}, artist_type_id={self.artist_type_id})>"

    def update_dias_apresentacao(self, dias: List[str]):
        """Atualizar dias de apresentação"""
        dias_validos = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        if not all(dia in dias_validos for dia in dias):
            raise ValueError("Dias de apresentação inválidos")
        self.dias_apresentacao = dias
        self.updated_at = datetime.utcnow()

    def update_raio_atuacao(self, raio: float):
        """Atualizar raio de atuação"""
        if raio <= 0:
            raise ValueError("Raio de atuação deve ser maior que zero")
        self.raio_atuacao = raio
        self.updated_at = datetime.utcnow()

    def update_duracao_apresentacao(self, duracao: float):
        """Atualizar duração da apresentação"""
        if duracao <= 0:
            raise ValueError("Duração da apresentação deve ser maior que zero")
        self.duracao_apresentacao = duracao
        self.updated_at = datetime.utcnow()

    def update_valor_hora(self, valor: float):
        """Atualizar valor por hora"""
        if valor < 0:
            raise ValueError("Valor por hora não pode ser negativo")
        self.valor_hora = valor
        self.updated_at = datetime.utcnow()

    def update_valor_couvert(self, valor: float):
        """Atualizar valor do couvert artístico"""
        if valor < 0:
            raise ValueError("Valor do couvert não pode ser negativo")
        self.valor_couvert = valor
        self.updated_at = datetime.utcnow()

    def update_requisitos_minimos(self, requisitos: str):
        """Atualizar requisitos mínimos"""
        if not requisitos or not requisitos.strip():
            raise ValueError("Requisitos mínimos não podem estar vazios")
        self.requisitos_minimos = requisitos.strip()
        self.updated_at = datetime.utcnow()

    def update_social_media(self, platform: str, url: Optional[str]):
        """Atualizar link de rede social"""
        valid_platforms = ["instagram", "tiktok", "youtube", "facebook", "soundcloud", "bandcamp", "spotify", "deezer"]
        if platform not in valid_platforms:
            raise ValueError(f"Plataforma inválida: {platform}")
        
        setattr(self, platform, url)
        self.updated_at = datetime.utcnow() 