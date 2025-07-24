from datetime import datetime, date
from typing import Optional
from enum import Enum

class StatusInterest(Enum):
    """Enum para status de interesse"""
    AGUARDANDO_CONFIRMACAO = "Aguardando Confirmação"
    ACEITO = "Aceito"
    RECUSADO = "Recusado"

class Interest:
    """Entidade de domínio para manifestações de interesse entre profiles"""
    
    def __init__(
        self,
        profile_id_interessado: int,
        profile_id_interesse: int,
        data_inicial: date,
        horario_inicial: str,
        duracao_apresentacao: float,
        valor_hora_ofertado: float,
        valor_couvert_ofertado: float,
        mensagem: str,
        space_event_type_id: Optional[int] = None,
        space_festival_type_id: Optional[int] = None,
        resposta: Optional[str] = None,
        status: StatusInterest = StatusInterest.AGUARDANDO_CONFIRMACAO,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.profile_id_interessado = profile_id_interessado
        self.profile_id_interesse = profile_id_interesse
        self.data_inicial = data_inicial
        self.horario_inicial = horario_inicial
        self.duracao_apresentacao = duracao_apresentacao
        self.valor_hora_ofertado = valor_hora_ofertado
        self.valor_couvert_ofertado = valor_couvert_ofertado
        self.space_event_type_id = space_event_type_id
        self.space_festival_type_id = space_festival_type_id
        self.mensagem = mensagem
        self.resposta = resposta
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Validações de negócio
        self._validate_profile_ids()
        self._validate_horario_inicial()
        self._validate_duracao_apresentacao()
        self._validate_valores_monetarios()
        self._validate_mensagem()
        self._validate_relationships()
        self._validate_resposta_status()
    
    def _validate_profile_ids(self):
        """Validar se os profile_ids são válidos e diferentes"""
        if not isinstance(self.profile_id_interessado, int) or self.profile_id_interessado <= 0:
            raise ValueError("ID do profile interessado deve ser um número inteiro positivo")
        
        if not isinstance(self.profile_id_interesse, int) or self.profile_id_interesse <= 0:
            raise ValueError("ID do profile de interesse deve ser um número inteiro positivo")
        
        if self.profile_id_interessado == self.profile_id_interesse:
            raise ValueError("Profile interessado e profile de interesse devem ser diferentes")
    
    def _validate_horario_inicial(self):
        """Validar formato do horário inicial (HH:MM)"""
        if not self.horario_inicial or not self.horario_inicial.strip():
            raise ValueError("Horário inicial é obrigatório")
        
        # Validar formato HH:MM
        import re
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', self.horario_inicial.strip()):
            raise ValueError("Horário inicial deve estar no formato HH:MM")
    
    def _validate_duracao_apresentacao(self):
        """Validar duração da apresentação"""
        if not isinstance(self.duracao_apresentacao, (int, float)) or self.duracao_apresentacao <= 0:
            raise ValueError("Duração da apresentação deve ser um número positivo")
        
        if self.duracao_apresentacao > 24:
            raise ValueError("Duração da apresentação não pode exceder 24 horas")
    
    def _validate_valores_monetarios(self):
        """Validar valores monetários oferecidos"""
        if not isinstance(self.valor_hora_ofertado, (int, float)) or self.valor_hora_ofertado < 0:
            raise ValueError("Valor-hora ofertado deve ser um número não negativo")
        
        if not isinstance(self.valor_couvert_ofertado, (int, float)) or self.valor_couvert_ofertado < 0:
            raise ValueError("Valor do couvert ofertado deve ser um número não negativo")
    
    def _validate_mensagem(self):
        """Validar mensagem enviada"""
        if not self.mensagem or not self.mensagem.strip():
            raise ValueError("Mensagem é obrigatória")
        
        if len(self.mensagem.strip()) < 10:
            raise ValueError("Mensagem deve ter pelo menos 10 caracteres")
        
        if len(self.mensagem.strip()) > 1000:
            raise ValueError("Mensagem não pode exceder 1000 caracteres")
    
    def _validate_relationships(self):
        """Validar que apenas um tipo de relacionamento pode estar definido"""
        relationships = [self.space_event_type_id, self.space_festival_type_id]
        defined_relationships = [rel for rel in relationships if rel is not None]
        
        if len(defined_relationships) > 1:
            raise ValueError("Apenas um tipo de relacionamento pode ser especificado por interesse")
        
        # Validar IDs positivos quando definidos
        if self.space_event_type_id is not None and self.space_event_type_id <= 0:
            raise ValueError("ID do space-event type deve ser maior que zero")
        
        if self.space_festival_type_id is not None and self.space_festival_type_id <= 0:
            raise ValueError("ID do space-festival type deve ser maior que zero")
    
    def _validate_resposta_status(self):
        """Validar consistência entre resposta e status"""
        if self.status == StatusInterest.AGUARDANDO_CONFIRMACAO:
            if self.resposta is not None and self.resposta.strip():
                raise ValueError("Resposta não deve estar presente quando status é 'Aguardando Confirmação'")
        else:
            # Para status ACEITO ou RECUSADO, resposta pode existir ou não (é opcional)
            if self.resposta is not None and len(self.resposta.strip()) > 1000:
                raise ValueError("Resposta não pode exceder 1000 caracteres")
    
    def aceitar(self, resposta: Optional[str] = None):
        """Aceitar o interesse"""
        self.status = StatusInterest.ACEITO
        if resposta:
            self.resposta = resposta.strip()
        self.updated_at = datetime.now()
        self._validate_resposta_status()
    
    def recusar(self, resposta: Optional[str] = None):
        """Recusar o interesse"""
        self.status = StatusInterest.RECUSADO
        if resposta:
            self.resposta = resposta.strip()
        self.updated_at = datetime.now()
        self._validate_resposta_status()
    
    def update_mensagem(self, nova_mensagem: str):
        """Atualizar mensagem (apenas se ainda estiver aguardando confirmação)"""
        if self.status != StatusInterest.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Mensagem só pode ser alterada quando status é 'Aguardando Confirmação'")
        
        old_mensagem = self.mensagem
        self.mensagem = nova_mensagem
        try:
            self._validate_mensagem()
            self.updated_at = datetime.now()
        except ValueError as e:
            self.mensagem = old_mensagem  # Reverter em caso de erro
            raise e
    
    def update_valores(self, novo_valor_hora: Optional[float] = None, novo_valor_couvert: Optional[float] = None):
        """Atualizar valores oferecidos (apenas se ainda estiver aguardando confirmação)"""
        if self.status != StatusInterest.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Valores só podem ser alterados quando status é 'Aguardando Confirmação'")
        
        old_valor_hora = self.valor_hora_ofertado
        old_valor_couvert = self.valor_couvert_ofertado
        
        if novo_valor_hora is not None:
            self.valor_hora_ofertado = novo_valor_hora
        if novo_valor_couvert is not None:
            self.valor_couvert_ofertado = novo_valor_couvert
        
        try:
            self._validate_valores_monetarios()
            self.updated_at = datetime.now()
        except ValueError as e:
            self.valor_hora_ofertado = old_valor_hora  # Reverter em caso de erro
            self.valor_couvert_ofertado = old_valor_couvert
            raise e
    
    def __str__(self):
        return f"Interest(id={self.id}, interessado={self.profile_id_interessado}, interesse={self.profile_id_interesse})"
    
    def __repr__(self):
        return (f"Interest(id={self.id}, profile_id_interessado={self.profile_id_interessado}, "
                f"profile_id_interesse={self.profile_id_interesse}, status={self.status.value})") 