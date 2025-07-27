from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MAX_REQUESTS: int = 5
    WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
