from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    openai_api_key: str
    google_api_key: str
    pinecone_api_key: str
    pinecone_index: str

    model_config = SettingsConfigDict(env_file="../.env")