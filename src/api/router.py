from fastapi import APIRouter
from src.api.letters import router as letters_router
from src.api.guesses import router as guesses_router
from src.api.auth import router as auth_router
from src.api.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(letters_router, prefix="/letters", tags=["letters"])
api_router.include_router(guesses_router, prefix="/guesses", tags=["guesses"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
