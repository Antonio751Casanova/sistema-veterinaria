from app.application.dtos.auth_dto import LoginResponse, VeterinariaLogin, VeterinariaResponse
from app.application.dtos.usuario_dto import UsuarioResponse
from app.domain.exceptions import UnauthorizedError
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.repositories.i_veterinaria_repository import IVeterinariaRepository
from app.domain.services.i_password_hasher import IPasswordHasher
from app.domain.services.i_token_service import ITokenService


class LoginUseCase:
    """Autentica por email/contraseña y emite el JWT."""

    def __init__(
        self,
        usuario_repo: IUsuarioRepository,
        veterinaria_repo: IVeterinariaRepository,
        hasher: IPasswordHasher,
        tokens: ITokenService,
    ):
        self._usuarios = usuario_repo
        self._veterinarias = veterinaria_repo
        self._hasher = hasher
        self._tokens = tokens

    def execute(self, credentials: VeterinariaLogin) -> LoginResponse:
        usuario = self._usuarios.get_active_by_email(credentials.email)

        if usuario and self._hasher.verify(credentials.password, usuario.hashed_password):
            veterinaria = self._veterinarias.get_by_id(usuario.veterinaria_id)
            token = self._tokens.create_token(usuario.id, veterinaria.id, usuario.rol)
            return LoginResponse(
                success=True,
                message="Login exitoso",
                token=token,
                veterinaria=VeterinariaResponse.model_validate(veterinaria),
                usuario=UsuarioResponse.model_validate(usuario),
            )

        # Compatibilidad: si inicia sesión con el email de la veterinaria
        veterinaria = self._veterinarias.get_by_email(credentials.email)
        if veterinaria and self._hasher.verify(credentials.password, veterinaria.hashed_password):
            usuarios_vet = [
                u for u in self._usuarios.list_by_veterinaria(veterinaria.id) if u.activo == 1
            ]
            fallback_user = next(
                (u for u in usuarios_vet if u.rol == "secretaria"),
                usuarios_vet[0] if usuarios_vet else None,
            )
            if fallback_user:
                token = self._tokens.create_token(fallback_user.id, veterinaria.id, fallback_user.rol)
                return LoginResponse(
                    success=True,
                    message="Login exitoso",
                    token=token,
                    veterinaria=VeterinariaResponse.model_validate(veterinaria),
                    usuario=UsuarioResponse.model_validate(fallback_user),
                )

        raise UnauthorizedError("Email o contraseña incorrectos")
