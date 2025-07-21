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
    users = db.query(UserModel).order_by(UserModel.id).all()
    roles = db.query(RoleModel).order_by(RoleModel.id).all()
    perfis = [
        {
            "user_id": users[0].id,
            "role_id": roles[0].id,
            "full_name": users[0].name,
            "artistic_name": "Alice Artista",
            "bio": "Artista de música popular.",
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
            "user_id": users[1].id,
            "role_id": roles[1].id,
            "full_name": users[1].name,
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
            "user_id": users[2].id,
            "role_id": roles[2].id,
            "full_name": users[2].name,
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
        }
    ]
    for perfil in perfis:
        db.add(ProfileModel(**perfil))
    db.commit()
    db.close()
    print("Perfis criados com sucesso!")

if __name__ == "__main__":
    main() 