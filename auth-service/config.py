from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str 
    jwt_algorithm: str
    jwt_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()