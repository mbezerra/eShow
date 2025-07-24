#!/usr/bin/env python3
"""
Script para popular a tabela interests com dados iniciais
seguindo as regras de negócio estabelecidas.

Regras:
- role_id = 1 (ADMIN): NUNCA manifesta interesse nem recebe
- role_id = 2 (ARTISTA): Pode manifestar interesse em ESPACO (role_id = 3)  
- role_id = 3 (ESPACO): Pode manifestar interesse em ARTISTA (role_id = 2)
- Status inicial sempre "Aguardando Confirmação"
"""

from datetime import date, timedelta
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.interest_model import InterestModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel
from domain.entities.interest import StatusInterest

def get_valid_profiles():
    """Obtém profiles válidos para manifestações de interesse (role_id 2 e 3)"""
    session = SessionLocal()
    try:
        # Obter profiles artistas (role_id = 2) e espaços (role_id = 3)
        artist_profiles = session.query(ProfileModel).filter(ProfileModel.role_id == 2).limit(5).all()
        space_profiles = session.query(ProfileModel).filter(ProfileModel.role_id == 3).limit(5).all()
        return artist_profiles, space_profiles
    finally:
        session.close()

def get_event_and_festival_types():
    """Obtém alguns space-event-types e space-festival-types para relacionamentos"""
    session = SessionLocal()
    try:
        space_event_types = session.query(SpaceEventTypeModel).limit(3).all()
        space_festival_types = session.query(SpaceFestivalTypeModel).limit(2).all()
        return space_event_types, space_festival_types
    finally:
        session.close()

def init_interests():
    session = SessionLocal()
    try:
        # Verificar se já existem interests
        existing_count = session.query(InterestModel).count()
        if existing_count > 0:
            print(f"❌ Tabela interests já possui {existing_count} registros")
            print("Execute o script de limpeza primeiro se necessário")
            return
        
        artist_profiles, space_profiles = get_valid_profiles()
        
        if not artist_profiles:
            print("❌ Nenhum profile com role ARTISTA encontrado")
            return
            
        if not space_profiles:
            print("❌ Nenhum profile com role ESPACO encontrado")
            return
        
        space_event_types, space_festival_types = get_event_and_festival_types()
        
        interests_data = []
        base_date = date.today() + timedelta(days=15)  # Apresentações futuras
        
        # 1. Artistas manifestando interesse em espaços
        print("📝 Criando manifestações de interesse de artistas para espaços...")
        
        for i, artist in enumerate(artist_profiles[:3]):  # Primeiros 3 artistas
            for j, space in enumerate(space_profiles[:2]):  # Primeiros 2 espaços
                event_date = base_date + timedelta(days=(i * 7) + (j * 3))
                
                # Interesse básico sem relacionamento específico
                interest_basic = {
                    'profile_id_interessado': artist.id,
                    'profile_id_interesse': space.id,
                    'data_inicial': event_date,
                    'horario_inicial': f"{18 + i}:00",  # Horários variados
                    'duracao_apresentacao': 2.5 + (i * 0.5),  # 2.5 a 3.5 horas
                    'valor_hora_ofertado': 150.0 + (i * 25),  # R$ 150 a R$ 200
                    'valor_couvert_ofertado': 20.0 + (j * 5),  # R$ 20 a R$ 25
                    'mensagem': f"Olá! Sou o artista {artist.full_name} e gostaria de me apresentar no seu espaço. Tenho experiência em apresentações ao vivo e acredito que posso contribuir com um show de qualidade para o seu público.",
                    'resposta': None,
                    'status': StatusInterest.AGUARDANDO_CONFIRMACAO,
                    'space_event_type_id': None,
                    'space_festival_type_id': None
                }
                interests_data.append(interest_basic)
                
                # Interesse relacionado a evento (se disponível)
                if space_event_types and j == 0:  # Apenas para o primeiro espaço
                    event_date_specific = event_date + timedelta(days=10)
                    interest_event = {
                        'profile_id_interessado': artist.id,
                        'profile_id_interesse': space.id,
                        'data_inicial': event_date_specific,
                        'horario_inicial': f"{20 + i}:30",
                        'duracao_apresentacao': 3.0,
                        'valor_hora_ofertado': 200.0 + (i * 20),
                        'valor_couvert_ofertado': 30.0,
                        'mensagem': f"Interessado em participar do evento {space_event_types[i % len(space_event_types)].tema}. Tenho repertório adequado e experiência em eventos similares.",
                        'resposta': None,
                        'status': StatusInterest.AGUARDANDO_CONFIRMACAO,
                        'space_event_type_id': space_event_types[i % len(space_event_types)].id,
                        'space_festival_type_id': None
                    }
                    interests_data.append(interest_event)
        
        # 2. Espaços manifestando interesse em artistas
        print("📝 Criando manifestações de interesse de espaços para artistas...")
        
        for i, space in enumerate(space_profiles[:2]):  # Primeiros 2 espaços
            for j, artist in enumerate(artist_profiles[:3]):  # Todos os artistas
                event_date = base_date + timedelta(days=20 + (i * 5) + j)
                
                # Interesse básico
                interest_basic = {
                    'profile_id_interessado': space.id,
                    'profile_id_interesse': artist.id,
                    'data_inicial': event_date,
                    'horario_inicial': f"{19 + j}:00",
                    'duracao_apresentacao': 2.0 + (j * 0.3),
                    'valor_hora_ofertado': 180.0 + (j * 15),
                    'valor_couvert_ofertado': 25.0 + (i * 5),
                    'mensagem': f"Olá {artist.artistic_name}! Somos o {space.full_name} e gostaríamos de convidá-lo para uma apresentação em nosso espaço. Acreditamos que seu estilo combina perfeitamente com nosso público.",
                    'resposta': None,
                    'status': StatusInterest.AGUARDANDO_CONFIRMACAO,
                    'space_event_type_id': None,
                    'space_festival_type_id': None
                }
                interests_data.append(interest_basic)
                
                # Interesse relacionado a festival (se disponível)
                if space_festival_types and i == 0 and j < 2:  # Apenas alguns casos
                    festival_date = event_date + timedelta(days=15)
                    interest_festival = {
                        'profile_id_interessado': space.id,
                        'profile_id_interesse': artist.id,
                        'data_inicial': festival_date,
                        'horario_inicial': f"{21 + j}:00",
                        'duracao_apresentacao': 4.0,
                        'valor_hora_ofertado': 250.0,
                        'valor_couvert_ofertado': 35.0,
                        'mensagem': f"Convite especial para participar do nosso festival {space_festival_types[j % len(space_festival_types)].tema}. Seria uma honra tê-lo conosco neste evento especial!",
                        'resposta': None,
                        'status': StatusInterest.AGUARDANDO_CONFIRMACAO,
                        'space_event_type_id': None,
                        'space_festival_type_id': space_festival_types[j % len(space_festival_types)].id
                    }
                    interests_data.append(interest_festival)
        
        # 3. Alguns interesses com status diferente de "Aguardando Confirmação"
        print("📝 Criando algumas manifestações com status aceito/recusado...")
        
        # Aceitar alguns interesses (simular interações passadas)
        if len(interests_data) >= 3:
            interests_data[0]['status'] = StatusInterest.ACEITO
            interests_data[0]['resposta'] = "Aceito! Vamos combinar os detalhes da apresentação."
            
            interests_data[1]['status'] = StatusInterest.RECUSADO
            interests_data[1]['resposta'] = "Obrigado pelo interesse, mas já temos agenda fechada para este período."
            
            interests_data[4]['status'] = StatusInterest.ACEITO
            interests_data[4]['resposta'] = "Perfeito! Seu perfil combina exatamente com o que procuramos."
        
        # Inserir no banco de dados
        print(f"📝 Inserindo {len(interests_data)} manifestações de interesse...")
        
        for interest_data in interests_data:
            interest = InterestModel(**interest_data)
            session.add(interest)
        
        session.commit()
        
        # Estatísticas finais
        total_count = session.query(InterestModel).count()
        pending_count = session.query(InterestModel).filter(InterestModel.status == StatusInterest.AGUARDANDO_CONFIRMACAO).count()
        accepted_count = session.query(InterestModel).filter(InterestModel.status == StatusInterest.ACEITO).count()
        rejected_count = session.query(InterestModel).filter(InterestModel.status == StatusInterest.RECUSADO).count()
        
        print(f"\n✅ Dados iniciais criados com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   • Total de manifestações: {total_count}")
        print(f"   • Aguardando confirmação: {pending_count}")
        print(f"   • Aceitas: {accepted_count}")
        print(f"   • Recusadas: {rejected_count}")
        
        # Estatísticas por tipo
        with_events = session.query(InterestModel).filter(InterestModel.space_event_type_id.isnot(None)).count()
        with_festivals = session.query(InterestModel).filter(InterestModel.space_festival_type_id.isnot(None)).count()
        basic = total_count - with_events - with_festivals
        
        print(f"   • Básicas (sem evento/festival): {basic}")
        print(f"   • Relacionadas a eventos: {with_events}")
        print(f"   • Relacionadas a festivais: {with_festivals}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("🎭 Inicializando dados da tabela interests...")
    init_interests()
    print("🎯 Script concluído!") 