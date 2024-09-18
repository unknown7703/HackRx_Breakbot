from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    google_api_key: str
    pinecone_api_key: str
    pinecone_index: str
    cohere_api_key: str
    groq_api_key_alt: str
    mail_gun_api_key: str
    mail_gun_domain: str
    model_config = SettingsConfigDict(env_file="../.env")