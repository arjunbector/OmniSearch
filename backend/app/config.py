from pydantic_settings import BaseSettings
from typing import List
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
    # Make sure this matches exactly what's in Google Cloud Console
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    GOOGLE_AUTH_SCOPES: List[str] = GOOGLE_OAUTH_SCOPES
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = "auth_token"
    # Set to False in production if using HTTPS
    COOKIE_SECURE: bool = False

    class Config:
        env_file = ROOT_DIR / ".env"
        case_sensitive = True

settings = Settings()

# Add this for debugging
if __name__ == "__main__":
    print(f"Looking for .env file at: {ROOT_DIR / '.env'}")
    print(f"File exists: {(ROOT_DIR / '.env').exists()}") 