from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.guesses import GuessCreate, GuessRead, GuessStats
from src.schemas.common import ApiResponse
from src.core.config.database import get_db_session
from src.core.config.deps import require_admin_user
from src.services.guesses_service import GuessesService
from src.utils.responses import success_response
from src.models.user import User

router = APIRouter()


@router.post("", response_model=ApiResponse[GuessRead])
async def create_guess(
    payload: GuessCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_admin_user),
) -> ApiResponse[GuessRead]:
    service = GuessesService()
    guess = await service.create(session, payload.letter_id, payload.guessed_name)
    return success_response(GuessRead.model_validate(guess))


@router.get("/stats", response_model=ApiResponse[GuessStats])
async def get_guess_stats(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_admin_user),
) -> ApiResponse[GuessStats]:
    service = GuessesService()
    stats = await service.stats(session)
    return success_response(GuessStats(**stats))
