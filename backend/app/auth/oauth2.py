from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows
from google.oauth2 import id_token
from google.auth.transport import requests
from app.config import settings, GOOGLE_OAUTH_SCOPES
from typing import Optional
import json

class OAuth2CookieBearer(OAuth2):
    def __init__(self):
        super().__init__(
            flows=OAuthFlows(
                authorizationCode={
                    "authorizationUrl": "https://accounts.google.com/o/oauth2/v2/auth",
                    "tokenUrl": "https://oauth2.googleapis.com/token",
                    "scopes": {scope: scope for scope in GOOGLE_OAUTH_SCOPES if scope != "openid"}
                }
            )
        )

    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get(settings.COOKIE_NAME)
        print(f"Cookies in request: {request.cookies}")
        print(f"Looking for cookie named: {settings.COOKIE_NAME}")
        print(f"Found token: {bool(token)}")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token

oauth2_scheme = OAuth2CookieBearer()

class GoogleAuth:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    async def verify_token(self, token: str = Depends(oauth2_scheme)) -> str:
        # Return the token directly instead of verifying with Google
        return token

google_auth = GoogleAuth() 