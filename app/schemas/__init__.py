# Módulo de schemas Pydantic para validação de dados
from .user import UserCreate, UserUpdate, UserResponse
from .role import RoleCreate, RoleUpdate, RoleResponse
from .profile import ProfileCreate, ProfileUpdate, ProfileResponse
from .artist_type import ArtistTypeCreate, ArtistTypeUpdate, ArtistTypeResponse
from .musical_style import MusicalStyleCreate, MusicalStyleUpdate, MusicalStyleResponse
from .artist import ArtistCreate, ArtistUpdate, ArtistResponse 