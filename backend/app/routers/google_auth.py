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
        
        # Create the response first
        redirect_response = RedirectResponse(
            url=settings.DASHBOARD_URL,
            status_code=status.HTTP_303_SEE_OTHER
        )
        
        # Set the cookie on the redirect response
        print(f"Setting cookie {settings.COOKIE_NAME} with token: \n{credentials.token}\n\n")
        redirect_response.set_cookie(
            key=settings.COOKIE_NAME,
            value=credentials.token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            domain=None,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax",
            path="/"
        )
        
        return redirect_response
        
    except Exception as e:
        print(f"Error in callback: {str(e)}")
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
        
        # Define the MIME types we want to filter
        mime_types = [
            'application/pdf',  # PDFs
            'application/vnd.google-apps.document',  # Google Docs
            'application/vnd.google-apps.spreadsheet',  # Google Sheets
        ]
        
        query = " or ".join([f"mimeType='{mime}'" for mime in mime_types])
        
        results = service.files().list(
            pageSize=50, 
            q=query,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink)"
        ).execute()
        
        # Format the files list with more readable type names
        formatted_files = []
        for file in results.get('files', []):
            file_type = {
                'application/pdf': 'PDF',
                'application/vnd.google-apps.document': 'Google Doc',
                'application/vnd.google-apps.spreadsheet': 'Google Sheet'
            }.get(file['mimeType'], file['mimeType'])
            
            formatted_files.append({
                'name': file['name'],
                'type': file_type,
                'modified': file['modifiedTime'],
                'viewLink': file.get('webViewLink', ''),
                'id': file['id']
            })
        
        return {
            "files": formatted_files
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