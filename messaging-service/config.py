from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://messaging_user:messaging_pass@localhost:5432/messaging_db"
    auth_service_url: str = "http://localhost:8001"
    listings_service_url: str = "http://localhost:8002"
    
    class Config:
        env_file = ".env"

settings = Settings()