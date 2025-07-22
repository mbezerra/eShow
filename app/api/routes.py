from fastapi import APIRouter
from app.api.endpoints import users, auth, roles, profiles, artist_types, musical_styles, artists, artist_musical_styles, space_types, event_types

api_router = APIRouter()

# Incluir rotas dos diferentes módulos
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(artist_types.router, prefix="/artist-types", tags=["artist_types"])
api_router.include_router(musical_styles.router, prefix="/musical-styles", tags=["musical_styles"])
api_router.include_router(artists.router, prefix="/artists", tags=["artists"])
api_router.include_router(artist_musical_styles.router, prefix="/artist-musical-styles", tags=["artist-musical-styles"])
api_router.include_router(space_types.router, prefix="/space-types", tags=["space_types"])
api_router.include_router(event_types.router, prefix="/event-types", tags=["event_types"]) 