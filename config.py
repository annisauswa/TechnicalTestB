from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "demo_collection"
    port: int = 6000
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() 

if __name__ == "__main__":
    print("Settings loaded successfully!")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Collection Name: {settings.collection_name}")
    print(f"Port Number: {settings.port}")