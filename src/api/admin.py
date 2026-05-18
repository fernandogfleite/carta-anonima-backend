from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config.database import get_db_session
from src.core.config.deps import require_admin_user
from src.schemas.common import ApiResponse
from src.services.admin_service import AdminService
from src.utils.responses import success_response
from src.schemas.letters import AdminLetterRead, LetterUpdate
from src.services.letters_service import LettersService

router = APIRouter(dependencies=[Depends(require_admin_user)])


@router.get("/summary", response_model=ApiResponse[dict])
async def admin_summary(
    session: AsyncSession = Depends(get_db_session),
) -> ApiResponse[dict]:
    service = AdminService()
    summary = await service.letters_summary(session)
    return success_response(summary)


@router.get("/letters", response_model=ApiResponse[list[AdminLetterRead]])
async def admin_list_letters(
    session: AsyncSession = Depends(get_db_session),
) -> ApiResponse[list[AdminLetterRead]]:
    service = LettersService()
    letters = await service.list(session)
    data = [AdminLetterRead.model_validate(letter) for letter in letters]
    return success_response(data)


@router.put("/letters/{letter_id}", response_model=ApiResponse[AdminLetterRead])
async def admin_update_letter(
    letter_id: int,
    payload: LetterUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> ApiResponse[AdminLetterRead]:
    service = LettersService()
    letter = await service.update(
        session,
        letter_id,
        payload.content,
        payload.anonymous_hint,
        payload.is_revealed,
        payload.is_solved,
    )
    return success_response(AdminLetterRead.model_validate(letter))


@router.delete("/letters/{letter_id}", response_model=ApiResponse[dict])
async def admin_delete_letter(
    letter_id: int, session: AsyncSession = Depends(get_db_session)
) -> ApiResponse[dict]:
    service = LettersService()
    await service.delete(session, letter_id)
    return success_response({"deleted": True})
