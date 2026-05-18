from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.letters import LetterCreate, LetterRead
from src.schemas.common import ApiResponse
from src.core.config.database import get_db_session
from src.core.config.deps import require_admin_user
from src.services.letters_service import LettersService
from src.utils.responses import success_response
from src.models.user import User

router = APIRouter()


@router.post("", response_model=ApiResponse[LetterRead])
async def create_letter(
    request: Request,
    payload: LetterCreate,
    session: AsyncSession = Depends(get_db_session),
) -> ApiResponse[LetterRead]:
    service = LettersService()
    sender_ip = request.client.host if request.client else "unknown"
    letter = await service.create(
        session, payload.content, payload.sender_name, payload.anonymous_hint, sender_ip
    )
    return success_response(LetterRead.model_validate(letter))


@router.get("", response_model=ApiResponse[list[LetterRead]])
async def list_letters(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_admin_user),
) -> ApiResponse[list[LetterRead]]:
    service = LettersService()
    letters = await service.list(session)
    data = [LetterRead.model_validate(letter) for letter in letters]
    return success_response(data)


@router.get("/random", response_model=ApiResponse[LetterRead])
async def get_random_letter(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_admin_user),
) -> ApiResponse[LetterRead]:
    service = LettersService()
    letter = await service.get_random(session)
    return success_response(LetterRead.model_validate(letter))


@router.get("/{letter_id}", response_model=ApiResponse[LetterRead])
async def get_letter(
    letter_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_admin_user),
) -> ApiResponse[LetterRead]:
    service = LettersService()
    letter = await service.get(session, letter_id)
    return success_response(LetterRead.model_validate(letter))
