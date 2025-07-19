from infrastructure.database.database import get_database_session
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.role_repository_impl import RoleRepositoryImpl
from app.application.services.user_service import UserService
from app.application.services.role_service import RoleService

def get_user_repository():
    """Dependency para obter o repositório de usuários"""
    session = next(get_database_session())
    return UserRepositoryImpl(session)

def get_user_service():
    """Dependency para obter o serviço de usuários"""
    user_repository = get_user_repository()
    return UserService(user_repository)

def get_role_repository():
    """Dependency para obter o repositório de roles"""
    session = next(get_database_session())
    return RoleRepositoryImpl(session)

def get_role_service():
    """Dependency para obter o serviço de roles"""
    role_repository = get_role_repository()
    return RoleService(role_repository) 