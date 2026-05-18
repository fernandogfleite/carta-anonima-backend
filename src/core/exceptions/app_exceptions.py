class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class NotFoundError(AppError):
    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(code, message, status_code=404, details=details)


class ValidationError(AppError):
    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(code, message, status_code=422, details=details)


class RateLimitError(AppError):
    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(code, message, status_code=429, details=details)


class AuthenticationError(AppError):
    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(code, message, status_code=401, details=details)


class AuthorizationError(AppError):
    def __init__(self, code: str, message: str, details: dict | None = None) -> None:
        super().__init__(code, message, status_code=403, details=details)
