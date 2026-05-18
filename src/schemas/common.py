from typing import Generic, TypeVar, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ErrorInfo(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: T | None = None
    error: ErrorInfo | None = None
