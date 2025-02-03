from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

# Get the root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define scopes as a constant to ensure consistency
GOOGLE_OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.readonly",
    "openid"
]

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_API_KEY: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    GOOGLE_AUTH_SCOPES: List[str] = GOOGLE_OAUTH_SCOPES
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = "auth_token"
    COOKIE_SECURE: bool = False  # Set to True only if using HTTPS
    COOKIE_SAMESITE: str = "lax"
    COOKIE_DOMAIN: Optional[str] = ""  # Empty string instead of None
    COOKIE_PATH: str = "/"
    
    # Dashboard redirect URL
    DASHBOARD_URL: str = "http://localhost:3000/dashboard"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ROOT_DIR / ".env"
        case_sensitive = True

settings = Settings()
