import os
import subprocess
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def get_git_version():
    """Obtém a versão atual do Git baseada na tag mais recente"""
    try:
        # Tenta obter a tag mais recente
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            # Remove o 'v' se presente (ex: v1.0.0 -> 1.0.0)
            if version.startswith('v'):
                version = version[1:]
            return version
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Fallback: tenta obter o hash do commit atual
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        if result.returncode == 0:
            return f"dev-{result.stdout.strip()}"
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Fallback final
    return "0.1.0"

class Settings:
    # Configurações da aplicação
    APP_NAME: str = os.getenv("APP_NAME", "eShow API")
    APP_VERSION: str = os.getenv("APP_VERSION", get_git_version())
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Configurações do banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./eshow.db")
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    @property
    def ACCESS_TOKEN_EXPIRE_DELTA(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    @property
    def REFRESH_TOKEN_EXPIRE_DELTA(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

settings = Settings() 