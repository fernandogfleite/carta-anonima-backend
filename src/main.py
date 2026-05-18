from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.api.router import api_router
from src.core.exceptions.app_exceptions import AppError
from src.utils.responses import error_response
from src.utils.logging import setup_logging
from src.core.config.database import SessionLocal
from src.services.auth_service import AuthService
from src.utils.jwt import decode_token
from jose import JWTError
import logging
from src.core.config.settings import get_settings


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()
    tags_metadata = [
        {"name": "auth", "description": "Autenticacao"},
        {"name": "letters", "description": "Cartas"},
        {"name": "guesses", "description": "Tentativas"},
        {"name": "admin", "description": "Administracao"},
    ]
    app = FastAPI(title="Cartas Anonimas", version="0.1.0", openapi_tags=tags_metadata)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(api_router)

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.code, exc.message, exc.details).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_response(
                "validation_error", "Erro de validacao", {"errors": exc.errors()}
            ).model_dump(),
        )

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        logger = logging.getLogger("api.request")
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            try:
                payload = decode_token(token)
                request.state.user_id = payload.get("sub")
                request.state.is_admin = payload.get("is_admin", False)
            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content=error_response(
                        "invalid_token", "Token invalido"
                    ).model_dump(),
                )
        response = await call_next(request)
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )
        return response

    @app.on_event("startup")
    async def bootstrap_admin() -> None:
        async with SessionLocal() as session:
            service = AuthService()
            await service.ensure_admin(session)

    return app


app = create_app()
