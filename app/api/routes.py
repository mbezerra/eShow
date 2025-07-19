from fastapi import APIRouter
from app.api.endpoints import users, auth

api_router = APIRouter()

# Incluir rotas dos diferentes módulos
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 