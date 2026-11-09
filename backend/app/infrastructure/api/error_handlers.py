from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    ConflictError, DomainError, ForbiddenError, NotFoundError,
    UnauthorizedError, ValidationError,
)

_STATUS_BY_ERROR = {
    ValidationError: 400,
    UnauthorizedError: 401,
    ForbiddenError: 403,
    NotFoundError: 404,
    ConflictError: 409,
}


def register_error_handlers(app: FastAPI) -> None:
    """Traduce excepciones de dominio al mismo formato {"detail": ...} que usaba HTTPException."""

    async def _handler(request: Request, exc: DomainError) -> JSONResponse:
        status_code = _STATUS_BY_ERROR.get(type(exc), 400)
        return JSONResponse(status_code=status_code, content={"detail": exc.message})

    app.add_exception_handler(DomainError, _handler)

