from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://listings_user:listings_pass@localhost:5432/listings_db"
    auth_service_url: str = "http://localhost:8001"
    
    class Config:
        env_file = ".env"

settings = Settings()