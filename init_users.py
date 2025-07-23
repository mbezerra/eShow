from infrastructure.database.database import SessionLocal
from infrastructure.database.models.user_model import UserModel
from app.core.security import get_password_hash

def main():
    db = SessionLocal()
    users = [
        {"name": "Admin eShow", "email": "admin@eshow.com", "password": get_password_hash("admin123"), "is_active": True},
        {"name": "Alice Silva", "email": "alice@example.com", "password": get_password_hash("senha123"), "is_active": True},
        {"name": "Bruno Souza", "email": "bruno@example.com", "password": get_password_hash("senha456"), "is_active": True},
        {"name": "Carla Lima", "email": "carla@example.com", "password": get_password_hash("senha789"), "is_active": True},
        # Novos usuários para espaços
        {"name": "Bar do Centro", "email": "bar.centro@example.com", "password": get_password_hash("espaco123"), "is_active": True},
        {"name": "Casa de Shows Musical", "email": "casa.musical@example.com", "password": get_password_hash("espaco456"), "is_active": True},
        {"name": "Pub Rock Station", "email": "pub.rock@example.com", "password": get_password_hash("espaco789"), "is_active": True},
    ]
    for user in users:
        if not db.query(UserModel).filter_by(email=user["email"]).first():
            db.add(UserModel(**user))
    db.commit()
    db.close()
    print("Usuários criados com sucesso!")

if __name__ == "__main__":
    main() 