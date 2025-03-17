import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings  

# Cargar variables de entorno
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "clave_por_defecto")
    DATABASE_URL: str = os.getenv("DATABASE_URL").replace("postgres://", "postgresql+asyncpg://", 1)
    OPTIMIZATION_SERVICE_URL: str = os.getenv("OPTIMIZATION_SERVICE_URL", "http://127.0.0.1:5000/optimize")
    OPTIMIZATION_MODE: str = os.getenv("OPTIMIZATION_MODE", "test")

settings = Settings()
