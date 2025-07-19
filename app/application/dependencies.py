from infrastructure.database.database import get_database_session
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.application.services.user_service import UserService

def get_user_repository():
    """Dependency para obter o repositório de usuários"""
    session = next(get_database_session())
    return UserRepositoryImpl(session)

def get_user_service():
    """Dependency para obter o serviço de usuários"""
    user_repository = get_user_repository()
    return UserService(user_repository) 