from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import google_auth
from app.config import settings, ROOT_DIR
import os

app = FastAPI(
    title="Omniverse Backend",
    description="Backend API for Omniverse",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]
)

# @app.on_event("startup")
# async def startup_event():

#     print("\nSettings values:")
#     try:
#         print(f"GOOGLE_CLIENT_ID: {settings.GOOGLE_CLIENT_ID}")
#         print(f"Has GOOGLE_CLIENT_SECRET: {bool(settings.GOOGLE_CLIENT_SECRET)}")
#         print(f"Has GOOGLE_API_KEY: {bool(settings.GOOGLE_API_KEY)}")
#         print(f"Has SECRET_KEY: {bool(settings.SECRET_KEY)}")
#     except Exception as e:
#         print(f"Error loading settings: {str(e)}")

# Include routers
app.include_router(google_auth.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 