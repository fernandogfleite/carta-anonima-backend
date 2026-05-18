from typing import Any, TypeVar
from src.schemas.common import ApiResponse, ErrorInfo

T = TypeVar("T")


def success_response(data: T | None = None) -> ApiResponse[T]:
    return ApiResponse(success=True, data=data)


def error_response(
    code: str, message: str, details: Any | None = None
) -> ApiResponse[None]:
    return ApiResponse(
        success=False, error=ErrorInfo(code=code, message=message, details=details)
    )
