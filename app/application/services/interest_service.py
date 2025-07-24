from typing import List, Optional, Union, Any
from datetime import date
from domain.repositories.interest_repository import InterestRepository
from domain.repositories.profile_repository import ProfileRepository
from domain.entities.interest import Interest, StatusInterest
from app.schemas.interest import InterestCreate, InterestUpdate, InterestStatusUpdate

class InterestService:
    """Serviço de aplicação para manifestações de interesse"""
    
    def __init__(self, interest_repository: InterestRepository, profile_repository: ProfileRepository):
        self.interest_repository = interest_repository
        self.profile_repository = profile_repository
    
    def create_interest(self, interest_data: InterestCreate) -> Interest:
        """Criar uma nova manifestação de interesse"""
        
        # Validar se os profiles existem
        profile_interessado = self.profile_repository.get_by_id(interest_data.profile_id_interessado)
        if not profile_interessado:
            raise ValueError(f"Profile interessado com ID {interest_data.profile_id_interessado} não encontrado")
        
        profile_interesse = self.profile_repository.get_by_id(interest_data.profile_id_interesse)
        if not profile_interesse:
            raise ValueError(f"Profile de interesse com ID {interest_data.profile_id_interesse} não encontrado")
        
        # Regras de negócio por role
        # Regra 1: ADMIN (role_id = 1) NUNCA manifesta interesse nem recebe
        if profile_interessado.role_id == 1:
            raise ValueError("Usuários com role ADMIN não podem manifestar interesse")
        
        if profile_interesse.role_id == 1:
            raise ValueError("Usuários com role ADMIN não podem receber manifestações de interesse")
        
        # Regra 2: ARTISTA (role_id = 2) pode manifestar interesse em ESPACO (role_id = 3)
        # Regra 3: ESPACO (role_id = 3) pode manifestar interesse em ARTISTA (role_id = 2)
        if profile_interessado.role_id == profile_interesse.role_id:
            raise ValueError("Não é possível manifestar interesse entre profiles do mesmo tipo de role")
        
        if profile_interessado.role_id == 2 and profile_interesse.role_id != 3:
            raise ValueError("Artistas só podem manifestar interesse em espaços")
        
        if profile_interessado.role_id == 3 and profile_interesse.role_id != 2:
            raise ValueError("Espaços só podem manifestar interesse em artistas")
        
        # Verificar se já existe interesse pendente entre os mesmo profiles
        existing_pending = self.interest_repository.get_by_profile_and_status(
            profile_id=interest_data.profile_id_interessado, 
            status=StatusInterest.AGUARDANDO_CONFIRMACAO, 
            is_interessado=True
        )
        
        for pending_interest in existing_pending:
            if hasattr(pending_interest, 'profile_id_interesse'):
                if pending_interest.profile_id_interesse == interest_data.profile_id_interesse:
                    raise ValueError("Já existe uma manifestação de interesse pendente entre estes profiles")
        
        interest = Interest(
            profile_id_interessado=interest_data.profile_id_interessado,
            profile_id_interesse=interest_data.profile_id_interesse,
            data_inicial=interest_data.data_inicial,
            horario_inicial=interest_data.horario_inicial,
            duracao_apresentacao=interest_data.duracao_apresentacao,
            valor_hora_ofertado=interest_data.valor_hora_ofertado,
            valor_couvert_ofertado=interest_data.valor_couvert_ofertado,
            space_event_type_id=interest_data.space_event_type_id,
            space_festival_type_id=interest_data.space_festival_type_id,
            mensagem=interest_data.mensagem,
            resposta=interest_data.resposta,
            status=interest_data.status
        )
        
        return self.interest_repository.create(interest)
    
    def get_interest_by_id(self, interest_id: int, include_relations: bool = False) -> Optional[Union[Interest, Any]]:
        """Obter uma manifestação de interesse por ID"""
        return self.interest_repository.get_by_id(interest_id, include_relations=include_relations)
    
    def get_interests_by_profile_interessado(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse feitas por um profile"""
        return self.interest_repository.get_by_profile_interessado(profile_id, include_relations=include_relations)
    
    def get_interests_by_profile_interesse(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse recebidas por um profile"""
        return self.interest_repository.get_by_profile_interesse(profile_id, include_relations=include_relations)
    
    def get_interests_by_status(self, status: StatusInterest, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse por status"""
        return self.interest_repository.get_by_status(status, include_relations=include_relations)
    
    def get_interests_by_space_event_type(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse relacionadas a um space-event type"""
        return self.interest_repository.get_by_space_event_type_id(space_event_type_id, include_relations=include_relations)
    
    def get_interests_by_space_festival_type(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse relacionadas a um space-festival type"""
        return self.interest_repository.get_by_space_festival_type_id(space_festival_type_id, include_relations=include_relations)
    
    def get_interests_by_date_range(self, data_inicio: date, data_fim: date, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse em um período"""
        return self.interest_repository.get_by_date_range(data_inicio, data_fim, include_relations=include_relations)
    
    def get_interests_by_profile_and_status(self, profile_id: int, status: StatusInterest, is_interessado: bool = True, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse de um profile filtradas por status"""
        return self.interest_repository.get_by_profile_and_status(profile_id, status, is_interessado, include_relations=include_relations)
    
    def get_pending_interests_for_profile(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter manifestações de interesse pendentes para um profile"""
        return self.interest_repository.get_pending_for_profile(profile_id, include_relations=include_relations)
    
    def get_interest_statistics(self, profile_id: int) -> dict:
        """Obter estatísticas de interesse para um profile"""
        return self.interest_repository.get_statistics_by_profile(profile_id)
    
    def update_interest(self, interest_id: int, interest_data: InterestUpdate) -> Optional[Interest]:
        """Atualizar uma manifestação de interesse"""
        # Obter o interesse atual
        existing = self.interest_repository.get_by_id(interest_id)
        if not existing:
            return None
        
        # Verificar se o interesse ainda pode ser alterado
        if hasattr(existing, 'status') and existing.status != StatusInterest.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Apenas interesses com status 'AGUARDANDO_CONFIRMACAO' podem ser alterados")
        
        # Criar entidade com os dados atualizados
        updated_interest = Interest(
            id=existing.id,
            profile_id_interessado=interest_data.profile_id_interessado if interest_data.profile_id_interessado is not None else existing.profile_id_interessado,
            profile_id_interesse=interest_data.profile_id_interesse if interest_data.profile_id_interesse is not None else existing.profile_id_interesse,
            data_inicial=interest_data.data_inicial if interest_data.data_inicial is not None else existing.data_inicial,
            horario_inicial=interest_data.horario_inicial if interest_data.horario_inicial is not None else existing.horario_inicial,
            duracao_apresentacao=interest_data.duracao_apresentacao if interest_data.duracao_apresentacao is not None else existing.duracao_apresentacao,
            valor_hora_ofertado=interest_data.valor_hora_ofertado if interest_data.valor_hora_ofertado is not None else existing.valor_hora_ofertado,
            valor_couvert_ofertado=interest_data.valor_couvert_ofertado if interest_data.valor_couvert_ofertado is not None else existing.valor_couvert_ofertado,
            space_event_type_id=interest_data.space_event_type_id if interest_data.space_event_type_id is not None else existing.space_event_type_id,
            space_festival_type_id=interest_data.space_festival_type_id if interest_data.space_festival_type_id is not None else existing.space_festival_type_id,
            mensagem=interest_data.mensagem if interest_data.mensagem is not None else existing.mensagem,
            resposta=interest_data.resposta if interest_data.resposta is not None else existing.resposta,
            status=interest_data.status if interest_data.status is not None else existing.status,
            created_at=existing.created_at,
            updated_at=existing.updated_at
        )
        
        return self.interest_repository.update(interest_id, updated_interest)
    
    def update_interest_status(self, interest_id: int, status_data: InterestStatusUpdate, user_profile_id: int) -> Optional[Interest]:
        """Atualizar status de uma manifestação de interesse (aceitar/recusar)"""
        # Obter o interesse atual
        existing = self.interest_repository.get_by_id(interest_id)
        if not existing:
            raise ValueError("Manifestação de interesse não encontrada")
        
        # Verificar se o usuário é a pessoa de interesse (quem pode aceitar/recusar)
        if hasattr(existing, 'profile_id_interesse') and existing.profile_id_interesse != user_profile_id:
            raise ValueError("Apenas a pessoa de interesse pode aceitar ou recusar a manifestação")
        
        # Verificar se o status atual permite alteração
        if hasattr(existing, 'status') and existing.status != StatusInterest.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Apenas interesses com status 'AGUARDANDO_CONFIRMACAO' podem ser aceitos ou recusados")
        
        # Criar entidade com status atualizado
        updated_interest = Interest(
            id=existing.id,
            profile_id_interessado=existing.profile_id_interessado,
            profile_id_interesse=existing.profile_id_interesse,
            data_inicial=existing.data_inicial,
            horario_inicial=existing.horario_inicial,
            duracao_apresentacao=existing.duracao_apresentacao,
            valor_hora_ofertado=existing.valor_hora_ofertado,
            valor_couvert_ofertado=existing.valor_couvert_ofertado,
            space_event_type_id=existing.space_event_type_id,
            space_festival_type_id=existing.space_festival_type_id,
            mensagem=existing.mensagem,
            resposta=status_data.resposta,
            status=status_data.status,
            created_at=existing.created_at,
            updated_at=existing.updated_at
        )
        
        return self.interest_repository.update(interest_id, updated_interest)
    
    def accept_interest(self, interest_id: int, user_profile_id: int, resposta: Optional[str] = None) -> Optional[Interest]:
        """Aceitar uma manifestação de interesse"""
        status_update = InterestStatusUpdate(
            status=StatusInterest.ACEITO,
            resposta=resposta
        )
        return self.update_interest_status(interest_id, status_update, user_profile_id)
    
    def reject_interest(self, interest_id: int, user_profile_id: int, resposta: Optional[str] = None) -> Optional[Interest]:
        """Recusar uma manifestação de interesse"""
        status_update = InterestStatusUpdate(
            status=StatusInterest.RECUSADO,
            resposta=resposta
        )
        return self.update_interest_status(interest_id, status_update, user_profile_id)
    
    def delete_interest(self, interest_id: int, user_profile_id: int) -> bool:
        """Deletar uma manifestação de interesse"""
        # Obter o interesse atual
        existing = self.interest_repository.get_by_id(interest_id)
        if not existing:
            return False
        
        # Verificar se o usuário é o interessado (só quem criou pode deletar)
        if hasattr(existing, 'profile_id_interessado') and existing.profile_id_interessado != user_profile_id:
            raise ValueError("Apenas quem manifestou o interesse pode deletá-lo")
        
        # Verificar se o status permite deleção (apenas pendentes)
        if hasattr(existing, 'status') and existing.status != StatusInterest.AGUARDANDO_CONFIRMACAO:
            raise ValueError("Apenas interesses com status 'AGUARDANDO_CONFIRMACAO' podem ser deletados")
        
        return self.interest_repository.delete(interest_id)
    
    def get_all_interests(self, include_relations: bool = False) -> List[Union[Interest, Any]]:
        """Obter todas as manifestações de interesse"""
        return self.interest_repository.get_all(include_relations=include_relations) 