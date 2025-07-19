from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        is_active: bool = True,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    def activate(self):
        """Ativar o usuário"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        """Desativar o usuário"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_name(self, new_name: str):
        """Atualizar o nome do usuário"""
        if not new_name or not new_name.strip():
            raise ValueError("Nome não pode estar vazio")
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()

    def update_email(self, new_email: str):
        """Atualizar o email do usuário"""
        if not new_email or '@' not in new_email:
            raise ValueError("Email inválido")
        self.email = new_email.lower()
        self.updated_at = datetime.utcnow() 