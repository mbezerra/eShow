from fastapi import APIRouter
from app.api.endpoints import users, auth, roles, profiles, artist_types, musical_styles, artists, artist_musical_styles, space_types, event_types, festival_types, spaces, space_event_types, space_festival_types, bookings, reviews, financials, interests, location_search

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
api_router.include_router(festival_types.router, prefix="/festival-types", tags=["festival_types"])
api_router.include_router(spaces.router, prefix="/spaces", tags=["spaces"])
api_router.include_router(space_event_types.router, prefix="/space-event-types", tags=["space-event-types"])
api_router.include_router(space_festival_types.router, prefix="/space-festival-types", tags=["space-festival-types"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(financials.router, prefix="/financials", tags=["financials"])
api_router.include_router(interests.router, prefix="/interests", tags=["interests"])
api_router.include_router(location_search.router, prefix="/location-search", tags=["location-search"]) 