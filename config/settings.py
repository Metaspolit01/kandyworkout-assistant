from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2000
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str = ""  # service_role key — bypasses RLS (used for seeding)
    
    # Notion
    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str
    
    # User Profile
    USER_NAME: str = "Karthik"
    USER_AGE: int = 20
    USER_HEIGHT_CM: int = 163
    USER_WEIGHT_KG: int = 58
    USER_LEVEL: str = "beginner"
    USER_GOAL: str = "Become an advanced calisthenics athlete"
    
    # Application
    LOG_LEVEL: str = "INFO"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Retry Configuration
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: float = 1.0


settings = Settings()
