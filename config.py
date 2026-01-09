from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "demo_collection"
    port: int = 6000
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() 