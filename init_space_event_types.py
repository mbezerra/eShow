#!/usr/bin/env python3
"""
Script para inicializar dados de Space Event Types no banco de dados
Popula a tabela space_event_types com relacionamentos iniciais

Este script cria relacionamentos N:N entre espaços e tipos de evento com
informações detalhadas como tema, descrição, data, horário e banners.

Execução:
    python init_space_event_types.py

Pré-requisitos:
    - Banco de dados inicializado
    - Tabelas spaces e event_types populadas
    - Migração space_event_types aplicada
"""

import sys
import os
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import get_database_session
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.event_type_model import EventTypeModel

def init_space_event_types():
    """Inicializar dados iniciais de Space Event Types"""
    db = next(get_database_session())
    
    try:
        # Verificar se já existem dados
        existing_count = db.query(SpaceEventTypeModel).count()
        if existing_count > 0:
            print(f"Já existem {existing_count} relacionamentos space-event-types no banco de dados.")
            return
        
        # Buscar alguns espaços e tipos de eventos para criar relacionamentos iniciais
        spaces = db.query(SpaceModel).limit(3).all()
        event_types = db.query(EventTypeModel).limit(3).all()
        
        if not spaces:
            print("Nenhum espaço encontrado. Execute primeiro init_spaces.py")
            return
            
        if not event_types:
            print("Nenhum tipo de evento encontrado. Execute primeiro init_event_types.py")
            return
        
        # Data base para os eventos (próximos 30 dias)
        base_date = datetime.now()
        
        # Dados iniciais de relacionamentos Space-Event Types
        space_event_types_data = [
            {
                "space_id": spaces[0].id,
                "event_type_id": event_types[0].id,
                "tema": "Noite de Jazz Clássico",
                "descricao": "Uma noite especial dedicada aos grandes clássicos do jazz, com apresentações de artistas locais e internacionais.",
                "link_divulgacao": "https://example.com/jazz-classico",
                "banner": "/static/banners/jazz-night.jpg",
                "data": base_date + timedelta(days=7),
                "horario": "20:00"
            },
            {
                "space_id": spaces[0].id,
                "event_type_id": event_types[1].id if len(event_types) > 1 else event_types[0].id,
                "tema": "Festival de Música Eletrônica",
                "descricao": "Festival com os melhores DJs da cidade apresentando diferentes estilos de música eletrônica.",
                "link_divulgacao": "https://example.com/eletronica-festival",
                "banner": "/static/banners/electronic-festival.jpg",
                "data": base_date + timedelta(days=14),
                "horario": "22:00"
            },
            {
                "space_id": spaces[1].id if len(spaces) > 1 else spaces[0].id,
                "event_type_id": event_types[0].id,
                "tema": "Sarau Cultural",
                "descricao": "Evento cultural com apresentações de música, poesia e teatro, promovendo artistas locais.",
                "link_divulgacao": None,
                "banner": None,
                "data": base_date + timedelta(days=21),
                "horario": "19:00"
            },
            {
                "space_id": spaces[1].id if len(spaces) > 1 else spaces[0].id,
                "event_type_id": event_types[2].id if len(event_types) > 2 else event_types[0].id,
                "tema": "Show Acústico Intimista",
                "descricao": "Apresentação acústica em ambiente intimista, proporcionando uma experiência musical única.",
                "link_divulgacao": "https://example.com/acustico",
                "banner": "/static/banners/acoustic-show.jpg",
                "data": base_date + timedelta(days=28),
                "horario": "21:30"
            },
            {
                "space_id": spaces[2].id if len(spaces) > 2 else spaces[0].id,
                "event_type_id": event_types[0].id,
                "tema": "Festa Junina Musical",
                "descricao": "Celebração junina com música típica, quadrilha e apresentações folclóricas.",
                "link_divulgacao": "https://example.com/festa-junina",
                "banner": "/static/banners/festa-junina.jpg",
                "data": base_date + timedelta(days=35),
                "horario": "18:00"
            }
        ]
        
        # Criar relacionamentos
        created_count = 0
        for data in space_event_types_data:
            space_event_type = SpaceEventTypeModel(**data)
            db.add(space_event_type)
            created_count += 1
        
        db.commit()
        print(f"✅ {created_count} relacionamentos space-event-types criados com sucesso!")
        
        # Exibir relacionamentos criados
        print("\n📋 Relacionamentos criados:")
        space_event_types = db.query(SpaceEventTypeModel).all()
        for rel in space_event_types:
            space = db.query(SpaceModel).filter(SpaceModel.id == rel.space_id).first()
            event_type = db.query(EventTypeModel).filter(EventTypeModel.id == rel.event_type_id).first()
            print(f"  • {rel.tema} - Espaço: {space.profile_id if space else 'N/A'} | Tipo: {event_type.type if event_type else 'N/A'} | Data: {rel.data.strftime('%d/%m/%Y')} às {rel.horario}")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar relacionamentos space-event-types: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando dados de Space Event Types...")
    init_space_event_types()
    print("✨ Processo concluído!") 