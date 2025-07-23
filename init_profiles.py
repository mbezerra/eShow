#!/usr/bin/env python3
"""
Script para inicializar a tabela de profiles
"""
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.role_model import RoleModel

def main():
    db = SessionLocal()
    # Buscar usuários e roles
    admin_role = db.query(RoleModel).filter_by(role="ADMIN").first()
    artist_role = db.query(RoleModel).filter_by(role="ARTISTA").first()
    space_role = db.query(RoleModel).filter_by(role="ESPACO").first()
    
    # Buscar usuários por email
    alice = db.query(UserModel).filter_by(email="alice@example.com").first()
    bruno = db.query(UserModel).filter_by(email="bruno@example.com").first()
    carla = db.query(UserModel).filter_by(email="carla@example.com").first()
    bar_centro = db.query(UserModel).filter_by(email="bar.centro@example.com").first()
    casa_musical = db.query(UserModel).filter_by(email="casa.musical@example.com").first()
    pub_rock = db.query(UserModel).filter_by(email="pub.rock@example.com").first()
    
    perfis = [
        {
            "user_id": alice.id,
            "role_id": admin_role.id,
            "full_name": alice.name,
            "artistic_name": "Alice Admin",
            "bio": "Administradora do sistema eShow.",
            "cep": "01001-000",
            "logradouro": "Rua das Flores",
            "numero": "100",
            "complemento": "Apto 1",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_fixo": "(11) 3333-1111",
            "telefone_movel": "(11) 99999-1111",
            "whatsapp": "(11) 99999-1111"
        },
        {
            "user_id": bruno.id,
            "role_id": artist_role.id,
            "full_name": bruno.name,
            "artistic_name": "Bruno Show",
            "bio": "Cantor sertanejo.",
            "cep": "02002-000",
            "logradouro": "Av. Brasil",
            "numero": "200",
            "complemento": "Casa",
            "cidade": "Campinas",
            "uf": "SP",
            "telefone_fixo": "(19) 3333-2222",
            "telefone_movel": "(19) 99999-2222",
            "whatsapp": "(19) 99999-2222"
        },
        {
            "user_id": carla.id,
            "role_id": space_role.id,
            "full_name": carla.name,
            "artistic_name": "Carla Espaço",
            "bio": "Gestora de espaço cultural.",
            "cep": "03003-000",
            "logradouro": "Rua do Teatro",
            "numero": "300",
            "complemento": "Sala 3",
            "cidade": "Santos",
            "uf": "SP",
            "telefone_fixo": "(13) 3333-3333",
            "telefone_movel": "(13) 99999-3333",
            "whatsapp": "(13) 99999-3333"
        },
        {
            "user_id": bar_centro.id,
            "role_id": space_role.id,
            "full_name": bar_centro.name,
            "artistic_name": "Bar do Centro",
            "bio": "Bar tradicional no centro da cidade com música ao vivo.",
            "cep": "04004-000",
            "logradouro": "Rua XV de Novembro",
            "numero": "150",
            "complemento": "Térreo",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_fixo": "(11) 3333-4444",
            "telefone_movel": "(11) 99999-4444",
            "whatsapp": "(11) 99999-4444"
        },
        {
            "user_id": casa_musical.id,
            "role_id": space_role.id,
            "full_name": casa_musical.name,
            "artistic_name": "Casa de Shows Musical",
            "bio": "Casa de shows especializada em música popular brasileira.",
            "cep": "05005-000",
            "logradouro": "Av. Paulista",
            "numero": "1000",
            "complemento": "Andar 2",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_fixo": "(11) 3333-5555",
            "telefone_movel": "(11) 99999-5555",
            "whatsapp": "(11) 99999-5555"
        },
        {
            "user_id": pub_rock.id,
            "role_id": space_role.id,
            "full_name": pub_rock.name,
            "artistic_name": "Pub Rock Station",
            "bio": "Pub especializado em rock e música alternativa.",
            "cep": "06006-000",
            "logradouro": "Rua Augusta",
            "numero": "500",
            "complemento": "Subsolo",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_fixo": "(11) 3333-6666",
            "telefone_movel": "(11) 99999-6666",
            "whatsapp": "(11) 99999-6666"
        }
    ]
    
    # Limpar profiles existentes para evitar duplicatas
    db.query(ProfileModel).delete()
    
    for perfil in perfis:
        db.add(ProfileModel(**perfil))
    db.commit()
    db.close()
    print("Perfis criados com sucesso!")

if __name__ == "__main__":
    main() 