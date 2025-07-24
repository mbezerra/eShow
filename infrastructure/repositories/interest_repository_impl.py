from typing import List, Optional, Union
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from domain.repositories.interest_repository import InterestRepository
from domain.entities.interest import Interest, StatusInterest
from infrastructure.database.models.interest_model import InterestModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel

class InterestRepositoryImpl(InterestRepository):
    """Implementação do repositório para manifestações de interesse"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _configure_relations(self, query, include_relations: bool = False):
        """Configurar relacionamentos para a query"""
        if include_relations:
            query = query.options(
                joinedload(InterestModel.profile_interessado),
                joinedload(InterestModel.profile_interesse),
                joinedload(InterestModel.space_event_type),
                joinedload(InterestModel.space_festival_type)
            )
        return query
    
    def create(self, interest: Interest) -> Interest:
        """Criar uma nova manifestação de interesse"""
        # Verificar se os profiles existem
        profile_interessado = self.db.query(ProfileModel).filter(ProfileModel.id == interest.profile_id_interessado).first()
        if not profile_interessado:
            raise ValueError(f"Profile interessado com ID {interest.profile_id_interessado} não encontrado")
        
        profile_interesse = self.db.query(ProfileModel).filter(ProfileModel.id == interest.profile_id_interesse).first()
        if not profile_interesse:
            raise ValueError(f"Profile de interesse com ID {interest.profile_id_interesse} não encontrado")
        
        # Verificar se os relacionamentos existem quando especificados
        if interest.space_event_type_id:
            space_event_type = self.db.query(SpaceEventTypeModel).filter(SpaceEventTypeModel.id == interest.space_event_type_id).first()
            if not space_event_type:
                raise ValueError(f"Space-Event Type com ID {interest.space_event_type_id} não encontrado")
        
        if interest.space_festival_type_id:
            space_festival_type = self.db.query(SpaceFestivalTypeModel).filter(SpaceFestivalTypeModel.id == interest.space_festival_type_id).first()
            if not space_festival_type:
                raise ValueError(f"Space-Festival Type com ID {interest.space_festival_type_id} não encontrado")
        
        # Criar a manifestação de interesse
        db_interest = InterestModel(
            profile_id_interessado=interest.profile_id_interessado,
            profile_id_interesse=interest.profile_id_interesse,
            data_inicial=interest.data_inicial,
            horario_inicial=interest.horario_inicial,
            duracao_apresentacao=interest.duracao_apresentacao,
            valor_hora_ofertado=interest.valor_hora_ofertado,
            valor_couvert_ofertado=interest.valor_couvert_ofertado,
            space_event_type_id=interest.space_event_type_id,
            space_festival_type_id=interest.space_festival_type_id,
            mensagem=interest.mensagem,
            resposta=interest.resposta,
            status=interest.status
        )
        
        self.db.add(db_interest)
        self.db.commit()
        self.db.refresh(db_interest)
        
        return self._to_entity(db_interest)
    
    def get_by_id(self, interest_id: int, include_relations: bool = False) -> Optional[Union[Interest, InterestModel]]:
        """Obter uma manifestação de interesse por ID"""
        query = self.db.query(InterestModel).filter(InterestModel.id == interest_id)
        query = self._configure_relations(query, include_relations)
        interest = query.first()
        
        if not interest:
            return None
        
        if include_relations:
            return interest  # Retorna o modelo com relacionamentos carregados
        return self._to_entity(interest)
    
    def get_by_profile_interessado(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter todas as manifestações de interesse feitas por um profile"""
        query = self.db.query(InterestModel).filter(InterestModel.profile_id_interessado == profile_id)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_profile_interesse(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter todas as manifestações de interesse recebidas por um profile"""
        query = self.db.query(InterestModel).filter(InterestModel.profile_id_interesse == profile_id)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_status(self, status: StatusInterest, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse por status"""
        query = self.db.query(InterestModel).filter(InterestModel.status == status)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_space_event_type_id(self, space_event_type_id: int, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse relacionadas a um space-event type"""
        query = self.db.query(InterestModel).filter(InterestModel.space_event_type_id == space_event_type_id)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_space_festival_type_id(self, space_festival_type_id: int, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse relacionadas a um space-festival type"""
        query = self.db.query(InterestModel).filter(InterestModel.space_festival_type_id == space_festival_type_id)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_date_range(self, data_inicio: date, data_fim: date, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse em um período"""
        query = self.db.query(InterestModel).filter(
            and_(
                InterestModel.data_inicial >= data_inicio,
                InterestModel.data_inicial <= data_fim
            )
        )
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_by_profile_and_status(self, profile_id: int, status: StatusInterest, is_interessado: bool = True, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse de um profile filtradas por status"""
        if is_interessado:
            query = self.db.query(InterestModel).filter(
                and_(
                    InterestModel.profile_id_interessado == profile_id,
                    InterestModel.status == status
                )
            )
        else:
            query = self.db.query(InterestModel).filter(
                and_(
                    InterestModel.profile_id_interesse == profile_id,
                    InterestModel.status == status
                )
            )
        
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_pending_for_profile(self, profile_id: int, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter manifestações de interesse pendentes para um profile (recebidas e aguardando confirmação)"""
        query = self.db.query(InterestModel).filter(
            and_(
                InterestModel.profile_id_interesse == profile_id,
                InterestModel.status == StatusInterest.AGUARDANDO_CONFIRMACAO
            )
        )
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def get_statistics_by_profile(self, profile_id: int) -> dict:
        """Obter estatísticas de interesse para um profile"""
        # Estatísticas como interessado (manifestações feitas)
        interessado_stats = self.db.query(
            InterestModel.status,
            func.count(InterestModel.id).label('count')
        ).filter(
            InterestModel.profile_id_interessado == profile_id
        ).group_by(InterestModel.status).all()
        
        # Estatísticas como pessoa de interesse (manifestações recebidas)
        interesse_stats = self.db.query(
            InterestModel.status,
            func.count(InterestModel.id).label('count')
        ).filter(
            InterestModel.profile_id_interesse == profile_id
        ).group_by(InterestModel.status).all()
        
        # Organizar dados
        interessado_dict = {str(status): count for status, count in interessado_stats}
        interesse_dict = {str(status): count for status, count in interesse_stats}
        
        return {
            "como_interessado": interessado_dict,
            "como_pessoa_interesse": interesse_dict,
            "total_manifestado": sum(interessado_dict.values()),
            "total_recebido": sum(interesse_dict.values())
        }
    
    def update(self, interest_id: int, interest: Interest) -> Optional[Interest]:
        """Atualizar uma manifestação de interesse"""
        db_interest = self.db.query(InterestModel).filter(InterestModel.id == interest_id).first()
        if not db_interest:
            return None
        
        # Atualizar campos
        db_interest.profile_id_interessado = interest.profile_id_interessado
        db_interest.profile_id_interesse = interest.profile_id_interesse
        db_interest.data_inicial = interest.data_inicial
        db_interest.horario_inicial = interest.horario_inicial
        db_interest.duracao_apresentacao = interest.duracao_apresentacao
        db_interest.valor_hora_ofertado = interest.valor_hora_ofertado
        db_interest.valor_couvert_ofertado = interest.valor_couvert_ofertado
        db_interest.space_event_type_id = interest.space_event_type_id
        db_interest.space_festival_type_id = interest.space_festival_type_id
        db_interest.mensagem = interest.mensagem
        db_interest.resposta = interest.resposta
        db_interest.status = interest.status
        
        self.db.commit()
        self.db.refresh(db_interest)
        
        return self._to_entity(db_interest)
    
    def delete(self, interest_id: int) -> bool:
        """Deletar uma manifestação de interesse"""
        db_interest = self.db.query(InterestModel).filter(InterestModel.id == interest_id).first()
        if not db_interest:
            return False
        
        self.db.delete(db_interest)
        self.db.commit()
        return True
    
    def get_all(self, include_relations: bool = False) -> List[Union[Interest, InterestModel]]:
        """Obter todas as manifestações de interesse"""
        query = self.db.query(InterestModel)
        query = self._configure_relations(query, include_relations)
        interests = query.all()
        
        if include_relations:
            return interests  # Retorna modelos com relacionamentos carregados
        return [self._to_entity(interest) for interest in interests]
    
    def _to_entity(self, model: InterestModel) -> Interest:
        """Converter modelo para entidade"""
        return Interest(
            id=model.id,
            profile_id_interessado=model.profile_id_interessado,
            profile_id_interesse=model.profile_id_interesse,
            data_inicial=model.data_inicial,
            horario_inicial=model.horario_inicial,
            duracao_apresentacao=model.duracao_apresentacao,
            valor_hora_ofertado=model.valor_hora_ofertado,
            valor_couvert_ofertado=model.valor_couvert_ofertado,
            space_event_type_id=model.space_event_type_id,
            space_festival_type_id=model.space_festival_type_id,
            mensagem=model.mensagem,
            resposta=model.resposta,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) 