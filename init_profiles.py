#!/usr/bin/env python3
"""
Script para inicializar a tabela de profiles
"""
from infrastructure.database.database import engine, Base
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.role_model import RoleModel
from infrastructure.database.models.profile_model import ProfileModel
from sqlalchemy.orm import sessionmaker

def init_profiles():
    """Inicializar tabela de profiles"""
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    print("Tabela de profiles criada com sucesso!")
    print("A tabela está pronta para receber dados.")

if __name__ == "__main__":
    init_profiles() 