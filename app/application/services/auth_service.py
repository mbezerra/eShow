from typing import Optional
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token, is_refresh_token
from app.application.services.user_service import UserService
from app.schemas.auth import UserLogin, UserRegister, Token
from app.schemas.user import UserCreate, UserResponse

# Blacklist global compartilhada entre todas as instâncias
_token_blacklist = set()

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Autenticar usuário com email e senha"""
        user = self.user_service.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        return user

    def register_user(self, user_data: UserRegister) -> UserResponse:
        """Registrar novo usuário"""
        # Verificar se o email já existe
        existing_user = self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email já está em uso")

        # Criar usuário com senha hasheada
        user_create = UserCreate(
            name=user_data.name,
            email=user_data.email,
            password=get_password_hash(user_data.password),
            is_active=user_data.is_active
        )
        
        return self.user_service.create_user(user_create)

    def login_user(self, user_data: UserLogin) -> Token:
        """Fazer login do usuário"""
        user = self.authenticate_user(user_data.email, user_data.password)
        if not user:
            raise ValueError("Email ou senha incorretos")
        
        if not user.is_active:
            raise ValueError("Usuário inativo")

        # Criar tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def logout_user(self, user_id: int) -> None:
        """Fazer logout do usuário (adicionar token à blacklist)"""
        # Em uma implementação mais robusta, você adicionaria o token atual à blacklist
        # Por simplicidade, apenas retornamos sucesso
        # Para implementar blacklist real, seria necessário:
        # 1. Receber o token atual no endpoint
        # 2. Adicionar à blacklist
        # 3. Verificar blacklist no middleware de autenticação
        pass

    def is_token_blacklisted(self, token: str) -> bool:
        """Verificar se token está na blacklist"""
        global _token_blacklist
        return token in _token_blacklist

    def add_token_to_blacklist(self, token: str) -> None:
        """Adicionar token à blacklist"""
        global _token_blacklist
        _token_blacklist.add(token)

    def refresh_access_token(self, refresh_token: str) -> Token:
        """Renovar token de acesso usando refresh token"""
        # Verificar se refresh token está na blacklist
        if self.is_token_blacklisted(refresh_token):
            raise ValueError("Refresh token foi invalidado")
        
        # Verificar refresh token
        payload = verify_token(refresh_token)
        if not payload or not is_refresh_token(payload):
            raise ValueError("Refresh token inválido")
        
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Refresh token inválido")
        
        # Verificar se usuário existe e está ativo
        user = self.user_service.get_user_by_id(int(user_id))
        if not user or not user.is_active:
            raise ValueError("Usuário não encontrado ou inativo")
        
        # Criar novos tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token
        ) 