#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
"""
from infrastructure.database.database import engine, Base
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.role_model import RoleModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.artist_type_model import ArtistTypeModel
from infrastructure.database.models.musical_style_model import MusicalStyleModel
from infrastructure.database.models.artist_model import ArtistModel

def init_database():
    """Criar todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_database() 