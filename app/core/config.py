from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    REDIS_HOST:str
    REDIS_PORT:int

    CELERY_BROKER:str
    CELERY_BACKEND:str
    GEMINI_API_KEY:str



    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()