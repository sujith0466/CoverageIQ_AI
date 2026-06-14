from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CoverageIQ AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str
    
    # LLM APIs
    GROQ_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

if not settings.GROQ_API_KEY and not settings.GEMINI_API_KEY:
    raise ValueError("FATAL ERROR: Neither GROQ_API_KEY nor GEMINI_API_KEY is configured. At least one must be provided.")
