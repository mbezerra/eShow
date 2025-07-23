from datetime import datetime
from typing import Optional

class Review:
    """Entidade de domínio para avaliações/reviews"""
    
    def __init__(
        self,
        profile_id: int,
        nota: int,
        depoimento: str,
        space_event_type_id: Optional[int] = None,
        space_festival_type_id: Optional[int] = None,
        data_hora: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.profile_id = profile_id
        self.space_event_type_id = space_event_type_id
        self.space_festival_type_id = space_festival_type_id
        self.data_hora = data_hora or datetime.now()
        self.nota = nota
        self.depoimento = depoimento
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Validações de negócio
        self._validate_nota()
        self._validate_profile_id()
        self._validate_depoimento()
        self._validate_relationships()
    
    def _validate_nota(self):
        """Validar se a nota está entre 1 e 5"""
        if not isinstance(self.nota, int) or self.nota < 1 or self.nota > 5:
            raise ValueError("Nota deve ser um número inteiro entre 1 e 5")
    
    def _validate_profile_id(self):
        """Validar se o profile_id é válido"""
        if not isinstance(self.profile_id, int) or self.profile_id <= 0:
            raise ValueError("ID do profile deve ser um número inteiro positivo")
    
    def _validate_depoimento(self):
        """Validar se o depoimento não está vazio"""
        if not self.depoimento or not self.depoimento.strip():
            raise ValueError("Depoimento não pode estar vazio")
        
        if len(self.depoimento.strip()) < 10:
            raise ValueError("Depoimento deve ter pelo menos 10 caracteres")
    
    def _validate_relationships(self):
        """Validar que apenas um tipo de relacionamento pode estar definido"""
        relationships = [self.space_event_type_id, self.space_festival_type_id]
        defined_relationships = [rel for rel in relationships if rel is not None]
        
        if len(defined_relationships) > 1:
            raise ValueError("Apenas um tipo de relacionamento pode ser especificado por review")
    
    def update_nota(self, nova_nota: int):
        """Atualizar a nota do review"""
        old_nota = self.nota
        self.nota = nova_nota
        try:
            self._validate_nota()
        except ValueError as e:
            self.nota = old_nota  # Reverter em caso de erro
            raise e
    
    def update_depoimento(self, novo_depoimento: str):
        """Atualizar o depoimento do review"""
        old_depoimento = self.depoimento
        self.depoimento = novo_depoimento
        try:
            self._validate_depoimento()
        except ValueError as e:
            self.depoimento = old_depoimento  # Reverter em caso de erro
            raise e
    
    def __str__(self):
        return f"Review(id={self.id}, profile_id={self.profile_id}, nota={self.nota})"
    
    def __repr__(self):
        return (f"Review(id={self.id}, profile_id={self.profile_id}, "
                f"nota={self.nota}, data_hora='{self.data_hora}')") 