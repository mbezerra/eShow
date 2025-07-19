from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.schemas.auth import UserLogin, UserRegister, Token, RefreshToken
from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserService
from app.application.dependencies import get_user_service
from app.core.auth import get_current_user
from app.schemas.user import UserResponse
from typing import Optional

router = APIRouter()

def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    """Dependency para obter o serviço de autenticação"""
    return AuthService(user_service)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Registrar novo usuário"""
    try:
        user = auth_service.register_user(user_data)
        # Fazer login automático após registro
        login_data = UserLogin(email=user_data.email, password=user_data.password)
        return auth_service.login_user(login_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Fazer login do usuário"""
    try:
        return auth_service.login_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout")
def logout(
    authorization: Optional[str] = Header(None),
    current_user: UserResponse = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Fazer logout do usuário (invalidar token)"""
    try:
        # Extrair token do header Authorization
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            # Adicionar token à blacklist
            auth_service.add_token_to_blacklist(token)
        
        return {"message": "Logout realizado com sucesso"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshToken,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Renovar token de acesso"""
    try:
        return auth_service.refresh_access_token(refresh_data.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) 