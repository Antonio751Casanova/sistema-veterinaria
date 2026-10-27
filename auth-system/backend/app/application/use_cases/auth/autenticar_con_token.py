from typing import Optional, Tuple

from app.domain.entities.usuario import Usuario
from app.domain.entities.veterinaria import Veterinaria
from app.domain.exceptions import UnauthorizedError
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.repositories.i_veterinaria_repository import IVeterinariaRepository
from app.domain.services.i_token_service import ITokenService


class AutenticarConTokenUseCase:
    """Resuelve el usuario y la veterinaria a partir del token JWT."""

    def __init__(
        self,
        usuario_repo: IUsuarioRepository,
        veterinaria_repo: IVeterinariaRepository,
        tokens: ITokenService,
    ):
        self._usuarios = usuario_repo
        self._veterinarias = veterinaria_repo
        self._tokens = tokens

    def execute(self, token: Optional[str]) -> Tuple[Usuario, Veterinaria]:
        if not token:
            raise UnauthorizedError("Token no proporcionado")

        payload = self._tokens.verify_token(token)
        if not payload:
            raise UnauthorizedError("Token inválido o expirado")

        usuario = self._usuarios.get_active_by_id(payload["usuario_id"])
        if not usuario:
            raise UnauthorizedError("Usuario no encontrado o inactivo")

        veterinaria = self._veterinarias.get_by_id(payload["veterinaria_id"])
        if not veterinaria:
            raise UnauthorizedError("Veterinaria no encontrada")

        return usuario, veterinaria

