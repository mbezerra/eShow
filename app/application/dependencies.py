from infrastructure.database.database import get_database_session
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.role_repository_impl import RoleRepositoryImpl
from infrastructure.repositories.profile_repository_impl import ProfileRepositoryImpl
from app.application.services.user_service import UserService
from app.application.services.role_service import RoleService
from app.application.services.profile_service import ProfileService
from domain.repositories.artist_type_repository import ArtistTypeRepository
from infrastructure.repositories.artist_type_repository_impl import ArtistTypeRepositoryImpl
from app.application.services.artist_type_service import ArtistTypeService
from domain.repositories.musical_style_repository import MusicalStyleRepository
from infrastructure.repositories.musical_style_repository_impl import MusicalStyleRepositoryImpl
from app.application.services.musical_style_service import MusicalStyleService
from fastapi import Depends

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

def get_profile_repository():
    """Dependency para obter o repositório de profiles"""
    session = next(get_database_session())
    return ProfileRepositoryImpl(session)

def get_profile_service():
    """Dependency para obter o serviço de profiles"""
    profile_repository = get_profile_repository()
    role_repository = get_role_repository()
    return ProfileService(profile_repository, role_repository)

def get_artist_type_repository(db=Depends(get_database_session)) -> ArtistTypeRepository:
    return ArtistTypeRepositoryImpl(db)

def get_artist_type_service(artist_type_repository: ArtistTypeRepository = Depends(get_artist_type_repository)) -> ArtistTypeService:
    return ArtistTypeService(artist_type_repository)

def get_musical_style_repository(db=Depends(get_database_session)) -> MusicalStyleRepository:
    return MusicalStyleRepositoryImpl(db)

def get_musical_style_service(musical_style_repository: MusicalStyleRepository = Depends(get_musical_style_repository)) -> MusicalStyleService:
    return MusicalStyleService(musical_style_repository) 