from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.config import settings
from app.auth.oauth2 import google_auth
from typing import Optional
import json

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

def create_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        },
        scopes=settings.GOOGLE_AUTH_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

@router.get("/login")
async def login():
    """Initiate Google OAuth2 login flow"""
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return RedirectResponse(authorization_url)

@router.get("/callback")
async def callback(code: str, request: Request, response: Response):
    """Handle OAuth2 callback from Google"""
    try:
        flow = create_flow()
        flow.fetch_token(code=code)
        
        credentials = flow.credentials
        if not credentials.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No refresh token received. Please ensure you have revoked access and try again."
            )
        
        # Create JSON response with token information
        token_info = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_type": "Bearer",
            "expires_in": credentials.expiry.timestamp() if credentials.expiry else None,
            "scope": credentials.scopes,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
        }
        
        # Set the cookie
        print(f"Setting cookie {settings.COOKIE_NAME} with token: \n{credentials.token}\n\n")
        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=credentials.token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            domain=None,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax",
            path="/"
        )
        
        # Return token information
        return token_info
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/drive/files")
async def list_files(request: Request, token: str = Depends(google_auth.verify_token)):
    """List files from user's Google Drive"""
    try:
        print(f"\nProcessing files request:")
        print(f"Token received: {token[:10]}...")
        
        credentials = Credentials(
            token=token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET
        )
        
        service = build('drive', 'v3', credentials=credentials)
        
        results = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
        ).execute()
        
        return {
            "files": results.get('files', [])
        }
        
    except Exception as e:
        print(f"Error in list_files: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/logout")
async def logout(response: Response):
    """Logout user by clearing the auth cookie"""
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        path="/",
        secure=settings.COOKIE_SECURE
    )
    return {"message": "Successfully logged out"} 