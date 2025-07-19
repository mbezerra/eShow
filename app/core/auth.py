from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token, is_access_token
from app.application.services.user_service import UserService
from app.application.dependencies import get_user_service
from app.application.services.auth_service import AuthService

security = HTTPBearer()

def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    """Dependency para obter o serviço de autenticação"""
    return AuthService(user_service)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Obter usuário atual baseado no token JWT"""
    token = credentials.credentials
    
    # Verificar se token está na blacklist
    if auth_service.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token foi invalidado (logout)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se é token de acesso
    if not is_access_token(payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obter usuário
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_service.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """Obter usuário atual ativo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user 