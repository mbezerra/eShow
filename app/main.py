from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="API construída com arquitetura hexagonal e autenticação JWT",
    version=settings.APP_VERSION
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (banners, imagens, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bem-vindo à eShow API - Arquitetura Hexagonal"}

from datetime import datetime

@app.get("/health")
async def health_check():
    current_year = datetime.now().year
    return {
        "status": "healthy", 
        "architecture": "hexagonal", 
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "copyright": f"© {current_year} eShow. Todos os direitos reservados."
    } 