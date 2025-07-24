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
from domain.repositories.artist_repository import ArtistRepository
from infrastructure.repositories.artist_repository_impl import ArtistRepositoryImpl
from app.application.services.artist_service import ArtistService
from domain.repositories.artist_musical_style_repository import ArtistMusicalStyleRepository
from infrastructure.repositories.artist_musical_style_repository_impl import ArtistMusicalStyleRepositoryImpl
from app.application.services.artist_musical_style_service import ArtistMusicalStyleService
from domain.repositories.space_type_repository import SpaceTypeRepository
from infrastructure.repositories.space_type_repository_impl import SpaceTypeRepositoryImpl
from app.application.services.space_type_service import SpaceTypeService
from domain.repositories.event_type_repository import EventTypeRepository
from infrastructure.repositories.event_type_repository_impl import EventTypeRepositoryImpl
from app.application.services.event_type_service import EventTypeService
from domain.repositories.festival_type_repository import FestivalTypeRepository
from infrastructure.repositories.festival_type_repository_impl import FestivalTypeRepositoryImpl
from app.application.services.festival_type_service import FestivalTypeService
from domain.repositories.space_repository import SpaceRepository
from infrastructure.repositories.space_repository_impl import SpaceRepositoryImpl
from app.application.services.space_service import SpaceService
from domain.repositories.space_event_type_repository import SpaceEventTypeRepository
from infrastructure.repositories.space_event_type_repository_impl import SpaceEventTypeRepositoryImpl
from app.application.services.space_event_type_service import SpaceEventTypeService
from domain.repositories.space_festival_type_repository import SpaceFestivalTypeRepository
from infrastructure.repositories.space_festival_type_repository_impl import SpaceFestivalTypeRepositoryImpl
from app.application.services.space_festival_type_service import SpaceFestivalTypeService
from domain.repositories.booking_repository import BookingRepository
from infrastructure.repositories.booking_repository_impl import BookingRepositoryImpl
from app.application.services.booking_service import BookingService
from domain.repositories.interest_repository import InterestRepository
from infrastructure.repositories.interest_repository_impl import InterestRepositoryImpl
from app.application.services.interest_service import InterestService
from fastapi import Depends

def get_user_repository(db=Depends(get_database_session)):
    """Dependency para obter o repositório de usuários"""
    return UserRepositoryImpl(db)

def get_user_service(user_repository: UserRepositoryImpl = Depends(get_user_repository)):
    """Dependency para obter o serviço de usuários"""
    return UserService(user_repository)

def get_role_repository(db=Depends(get_database_session)):
    """Dependency para obter o repositório de roles"""
    return RoleRepositoryImpl(db)

def get_role_service(role_repository: RoleRepositoryImpl = Depends(get_role_repository)):
    """Dependency para obter o serviço de roles"""
    return RoleService(role_repository)

def get_profile_repository(db=Depends(get_database_session)):
    """Dependency para obter o repositório de profiles"""
    return ProfileRepositoryImpl(db)

def get_profile_service(
    profile_repository: ProfileRepositoryImpl = Depends(get_profile_repository),
    role_repository: RoleRepositoryImpl = Depends(get_role_repository)
):
    """Dependency para obter o serviço de profiles"""
    return ProfileService(profile_repository, role_repository)

def get_artist_type_repository(db=Depends(get_database_session)) -> ArtistTypeRepository:
    return ArtistTypeRepositoryImpl(db)

def get_artist_type_service(artist_type_repository: ArtistTypeRepository = Depends(get_artist_type_repository)) -> ArtistTypeService:
    return ArtistTypeService(artist_type_repository)

def get_musical_style_repository(db=Depends(get_database_session)) -> MusicalStyleRepository:
    return MusicalStyleRepositoryImpl(db)

def get_musical_style_service(musical_style_repository: MusicalStyleRepository = Depends(get_musical_style_repository)) -> MusicalStyleService:
    return MusicalStyleService(musical_style_repository)

def get_artist_repository(db=Depends(get_database_session)) -> ArtistRepository:
    return ArtistRepositoryImpl(db)

def get_artist_service(
    artist_repository: ArtistRepository = Depends(get_artist_repository),
    profile_repository = Depends(get_profile_repository)
) -> ArtistService:
    return ArtistService(artist_repository, profile_repository)

def get_artist_musical_style_repository(db=Depends(get_database_session)) -> ArtistMusicalStyleRepository:
    return ArtistMusicalStyleRepositoryImpl(db)

def get_artist_musical_style_service(artist_musical_style_repository: ArtistMusicalStyleRepository = Depends(get_artist_musical_style_repository)) -> ArtistMusicalStyleService:
    return ArtistMusicalStyleService(artist_musical_style_repository)

def get_space_type_repository(db=Depends(get_database_session)) -> SpaceTypeRepository:
    return SpaceTypeRepositoryImpl(db)

def get_space_type_service(space_type_repository: SpaceTypeRepository = Depends(get_space_type_repository)) -> SpaceTypeService:
    return SpaceTypeService(space_type_repository)

def get_event_type_repository(db=Depends(get_database_session)) -> EventTypeRepository:
    return EventTypeRepositoryImpl(db)

def get_event_type_service(event_type_repository: EventTypeRepository = Depends(get_event_type_repository)) -> EventTypeService:
    return EventTypeService(event_type_repository)

def get_festival_type_repository(db=Depends(get_database_session)) -> FestivalTypeRepository:
    return FestivalTypeRepositoryImpl(db)

def get_festival_type_service(festival_type_repository: FestivalTypeRepository = Depends(get_festival_type_repository)) -> FestivalTypeService:
    return FestivalTypeService(festival_type_repository)

def get_space_repository(db=Depends(get_database_session)) -> SpaceRepository:
    return SpaceRepositoryImpl(db)

def get_space_service(
    space_repository: SpaceRepository = Depends(get_space_repository),
    profile_repository = Depends(get_profile_repository)
) -> SpaceService:
    return SpaceService(space_repository, profile_repository)

def get_space_event_type_repository(db=Depends(get_database_session)) -> SpaceEventTypeRepository:
    return SpaceEventTypeRepositoryImpl(db)

def get_space_event_type_service(space_event_type_repository: SpaceEventTypeRepository = Depends(get_space_event_type_repository)) -> SpaceEventTypeService:
    return SpaceEventTypeService(space_event_type_repository)

def get_space_festival_type_repository(db=Depends(get_database_session)) -> SpaceFestivalTypeRepository:
    return SpaceFestivalTypeRepositoryImpl(db)

def get_space_festival_type_service(space_festival_type_repository: SpaceFestivalTypeRepository = Depends(get_space_festival_type_repository)) -> SpaceFestivalTypeService:
    return SpaceFestivalTypeService(space_festival_type_repository)

def get_booking_repository(db=Depends(get_database_session)) -> BookingRepository:
    return BookingRepositoryImpl(db)

def get_booking_service(
    booking_repository: BookingRepository = Depends(get_booking_repository),
    profile_repository = Depends(get_profile_repository)
) -> BookingService:
    return BookingService(booking_repository, profile_repository)

def get_interest_repository(db=Depends(get_database_session)) -> InterestRepository:
    return InterestRepositoryImpl(db)

def get_interest_service(
    interest_repository: InterestRepository = Depends(get_interest_repository),
    profile_repository = Depends(get_profile_repository)
) -> InterestService:
    return InterestService(interest_repository, profile_repository) 