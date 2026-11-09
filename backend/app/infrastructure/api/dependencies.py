"""Composición de dependencias (inyección) y autenticación para la capa API."""
from typing import Optional

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.use_cases.auth import (
    AutenticarConTokenUseCase, LoginUseCase, RegistrarVeterinariaUseCase,
)
from app.application.use_cases.clientes import (
    ActualizarClienteUseCase, CrearClienteUseCase, EliminarClienteUseCase,
    ListarClientesUseCase, ObtenerClienteUseCase,
)
from app.application.use_cases.mascotas import (
    ActualizarMascotaUseCase, CrearMascotaUseCase, EliminarMascotaUseCase,
    ListarMascotasClienteUseCase, ListarTodasMascotasUseCase, ObtenerMascotaUseCase,
)
from app.application.use_cases.usuarios import (
    ActualizarUsuarioUseCase, CrearUsuarioUseCase, DesactivarUsuarioUseCase,
    ListarUsuariosUseCase,
)
from app.domain.entities.usuario import Usuario
from app.domain.entities.veterinaria import Veterinaria
from app.domain.exceptions import ForbiddenError
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories.cliente_repository import SqlAlchemyClienteRepository
from app.infrastructure.persistence.repositories.mascota_repository import SqlAlchemyMascotaRepository
from app.infrastructure.persistence.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.infrastructure.persistence.repositories.veterinaria_repository import SqlAlchemyVeterinariaRepository
from app.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.security.jwt_service import JwtTokenService
from app.infrastructure.security.password_hasher import PasslibPasswordHasher

__all__ = ["get_db", "CurrentUser", "get_current_user", "require_role"]

bearer_scheme = HTTPBearer(auto_error=False)


# ==================== Servicios y repositorios ====================

def _hasher() -> PasslibPasswordHasher:
    return PasslibPasswordHasher()


def _tokens() -> JwtTokenService:
    return JwtTokenService()


def _uow(db: Session) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(db)


# ==================== Autenticación ====================

class CurrentUser:
    """Contenedor con datos del usuario autenticado"""
    def __init__(self, usuario: Usuario, veterinaria: Veterinaria):
        self.usuario = usuario
        self.veterinaria = veterinaria
        self.veterinaria_id = veterinaria.id
        self.rol = usuario.rol
        self.usuario_id = usuario.id


def _extract_bearer_token(
    authorization: Optional[str],
    credentials: Optional[HTTPAuthorizationCredentials],
) -> Optional[str]:
    """Extrae y limpia el token JWT desde HTTPBearer o desde el header Authorization."""
    raw_token: Optional[str] = None

    if isinstance(credentials, HTTPAuthorizationCredentials) and credentials.credentials:
        raw_token = credentials.credentials
    elif isinstance(authorization, str) and authorization.strip():
        auth_val = authorization.strip()
        if auth_val.lower().startswith("bearer "):
            raw_token = auth_val[7:].strip()
        else:
            raw_token = auth_val

    if not raw_token:
        return None

    cleaned = raw_token.strip().strip('"').strip("'")
    if not cleaned or cleaned.lower() in ("null", "undefined", "none"):
        return None

    return cleaned


def get_current_user(
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> CurrentUser:
    """Obtener usuario actual desde el token JWT"""
    token = _extract_bearer_token(authorization, credentials)

    use_case = AutenticarConTokenUseCase(
        SqlAlchemyUsuarioRepository(db), SqlAlchemyVeterinariaRepository(db), _tokens()
    )
    usuario, veterinaria = use_case.execute(token)
    return CurrentUser(usuario=usuario, veterinaria=veterinaria)


def require_role(*roles: str):
    """Factory de dependencia que verifica el rol del usuario"""
    def _checker(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current.rol not in roles:
            raise ForbiddenError(f"Acceso denegado. Se requiere rol: {', '.join(roles)}")
        return current
    return _checker


# ==================== Proveedores de casos de uso ====================

def registrar_veterinaria_uc(db: Session = Depends(get_db)) -> RegistrarVeterinariaUseCase:
    return RegistrarVeterinariaUseCase(
        SqlAlchemyVeterinariaRepository(db), SqlAlchemyUsuarioRepository(db), _hasher(), _uow(db)
    )


def login_uc(db: Session = Depends(get_db)) -> LoginUseCase:
    return LoginUseCase(
        SqlAlchemyUsuarioRepository(db), SqlAlchemyVeterinariaRepository(db), _hasher(), _tokens()
    )


def listar_usuarios_uc(db: Session = Depends(get_db)) -> ListarUsuariosUseCase:
    return ListarUsuariosUseCase(SqlAlchemyUsuarioRepository(db))


def crear_usuario_uc(db: Session = Depends(get_db)) -> CrearUsuarioUseCase:
    return CrearUsuarioUseCase(SqlAlchemyUsuarioRepository(db), _hasher(), _uow(db))


def actualizar_usuario_uc(db: Session = Depends(get_db)) -> ActualizarUsuarioUseCase:
    return ActualizarUsuarioUseCase(SqlAlchemyUsuarioRepository(db), _hasher(), _uow(db))


def desactivar_usuario_uc(db: Session = Depends(get_db)) -> DesactivarUsuarioUseCase:
    return DesactivarUsuarioUseCase(SqlAlchemyUsuarioRepository(db), _uow(db))


def crear_cliente_uc(db: Session = Depends(get_db)) -> CrearClienteUseCase:
    return CrearClienteUseCase(SqlAlchemyClienteRepository(db), _uow(db))


def listar_clientes_uc(db: Session = Depends(get_db)) -> ListarClientesUseCase:
    return ListarClientesUseCase(SqlAlchemyClienteRepository(db))


def obtener_cliente_uc(db: Session = Depends(get_db)) -> ObtenerClienteUseCase:
    return ObtenerClienteUseCase(SqlAlchemyClienteRepository(db))


def actualizar_cliente_uc(db: Session = Depends(get_db)) -> ActualizarClienteUseCase:
    return ActualizarClienteUseCase(SqlAlchemyClienteRepository(db), _uow(db))


def eliminar_cliente_uc(db: Session = Depends(get_db)) -> EliminarClienteUseCase:
    return EliminarClienteUseCase(SqlAlchemyClienteRepository(db), _uow(db))


def crear_mascota_uc(db: Session = Depends(get_db)) -> CrearMascotaUseCase:
    return CrearMascotaUseCase(
        SqlAlchemyMascotaRepository(db), SqlAlchemyClienteRepository(db), _uow(db)
    )


def listar_mascotas_cliente_uc(db: Session = Depends(get_db)) -> ListarMascotasClienteUseCase:
    return ListarMascotasClienteUseCase(SqlAlchemyMascotaRepository(db), SqlAlchemyClienteRepository(db))


def listar_todas_mascotas_uc(db: Session = Depends(get_db)) -> ListarTodasMascotasUseCase:
    return ListarTodasMascotasUseCase(SqlAlchemyMascotaRepository(db))


def obtener_mascota_uc(db: Session = Depends(get_db)) -> ObtenerMascotaUseCase:
    return ObtenerMascotaUseCase(SqlAlchemyMascotaRepository(db))


def actualizar_mascota_uc(db: Session = Depends(get_db)) -> ActualizarMascotaUseCase:
    return ActualizarMascotaUseCase(SqlAlchemyMascotaRepository(db), _uow(db))


def eliminar_mascota_uc(db: Session = Depends(get_db)) -> EliminarMascotaUseCase:
    return EliminarMascotaUseCase(SqlAlchemyMascotaRepository(db), _uow(db))
