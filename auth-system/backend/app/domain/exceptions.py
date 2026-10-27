"""Excepciones de dominio. La capa de API las traduce a respuestas HTTP."""


class DomainError(Exception):
    """Error base de dominio."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(DomainError):
    """Datos inválidos o regla de negocio violada (HTTP 400)."""


class UnauthorizedError(DomainError):
    """Credenciales/token inválidos (HTTP 401)."""


class ForbiddenError(DomainError):
    """Sin permisos suficientes (HTTP 403)."""


class NotFoundError(DomainError):
    """Recurso inexistente (HTTP 404)."""


class ConflictError(DomainError):
    """Conflicto con el estado actual (HTTP 409)."""

