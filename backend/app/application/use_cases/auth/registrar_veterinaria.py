from app.application.dtos.auth_dto import VeterinariaCreate
from app.domain.entities.usuario import Usuario, ROL_SECRETARIA
from app.domain.entities.veterinaria import Veterinaria
from app.domain.exceptions import ValidationError
from app.domain.repositories.i_unit_of_work import IUnitOfWork
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.repositories.i_veterinaria_repository import IVeterinariaRepository
from app.domain.services.i_password_hasher import IPasswordHasher


class RegistrarVeterinariaUseCase:
    """Registra una veterinaria y su primer usuario (secretaria) en una sola transacción."""

    def __init__(
        self,
        veterinaria_repo: IVeterinariaRepository,
        usuario_repo: IUsuarioRepository,
        hasher: IPasswordHasher,
        uow: IUnitOfWork,
    ):
        self._veterinarias = veterinaria_repo
        self._usuarios = usuario_repo
        self._hasher = hasher
        self._uow = uow

    def execute(self, data: VeterinariaCreate) -> Veterinaria:
        if self._veterinarias.get_by_email(data.email):
            raise ValidationError("El email ya está registrado")

        hashed_pwd = self._hasher.hash(data.password)
        veterinaria = self._veterinarias.add(Veterinaria(
            nombre=data.nombre,
            telefono=data.telefono,
            direccion=data.direccion,
            email=data.email,
            hashed_password=hashed_pwd,
        ))

        # Usuario inicial con rol secretaria usando las mismas credenciales
        self._usuarios.add(Usuario(
            nombre=data.nombre,
            email=data.email,
            hashed_password=hashed_pwd,
            rol=ROL_SECRETARIA,
            activo=1,
            veterinaria_id=veterinaria.id,
        ))
        self._uow.commit()
        return veterinaria

