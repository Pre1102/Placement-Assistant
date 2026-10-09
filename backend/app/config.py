import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerCampusAI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Environment & Secrets
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'careercampus.db').replace(os.sep, '/')}")
    VECTORSTORE_DIR: str = os.getenv("VECTORSTORE_DIR", os.path.join(BASE_DIR, "vectorstore"))
    DATA_DIR: str = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data", "demo"))
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
