from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config.database import get_db_session
from src.schemas.auth import LoginRequest, TokenResponse
from src.schemas.common import ApiResponse
from src.services.auth_service import AuthService
from src.utils.responses import success_response

router = APIRouter()


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(
    payload: LoginRequest, session: AsyncSession = Depends(get_db_session)
) -> ApiResponse[TokenResponse]:
    service = AuthService()
    token = await service.authenticate(session, payload.email, payload.password)
    return success_response(TokenResponse(access_token=token))
