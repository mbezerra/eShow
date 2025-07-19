#!/usr/bin/env python3
"""
Script para inicializar a tabela de roles
"""
from infrastructure.database.database import engine, Base
from infrastructure.database.models.role_model import RoleModel
from domain.entities.role import RoleType
from sqlalchemy.orm import sessionmaker

def init_roles():
    """Inicializar tabela de roles com dados padrão"""
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    # Criar sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Verificar se já existem roles
        existing_roles = session.query(RoleModel).count()
        if existing_roles > 0:
            print("Tabela de roles já possui dados. Pulando inicialização.")
            return
        
        # Criar roles padrão
        roles = [
            RoleModel(role=RoleType.ADMIN),
            RoleModel(role=RoleType.ARTISTA),
            RoleModel(role=RoleType.ESPACO)
        ]
        
        session.add_all(roles)
        session.commit()
        
        print("Roles inicializados com sucesso:")
        for role in roles:
            print(f"  - ID: {role.id}, Role: {role.role.value}")
            
    except Exception as e:
        print(f"Erro ao inicializar roles: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_roles() 