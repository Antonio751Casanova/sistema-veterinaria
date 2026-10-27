from typing import List

from app.application.dtos.usuario_dto import UsuarioCreate
from app.domain.entities.usuario import Usuario, ROLES_VALIDOS
from app.domain.exceptions import NotFoundError, ValidationError
from app.domain.repositories.i_unit_of_work import IUnitOfWork
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.domain.services.i_password_hasher import IPasswordHasher


class ListarUsuariosUseCase:
    def __init__(self, usuario_repo: IUsuarioRepository):
        self._usuarios = usuario_repo

    def execute(self, veterinaria_id: int) -> List[Usuario]:
        return self._usuarios.list_by_veterinaria(veterinaria_id)


class CrearUsuarioUseCase:
    def __init__(self, usuario_repo: IUsuarioRepository, hasher: IPasswordHasher, uow: IUnitOfWork):
        self._usuarios = usuario_repo
        self._hasher = hasher
        self._uow = uow

    def execute(self, data: UsuarioCreate, veterinaria_id: int) -> Usuario:
        if data.rol not in ROLES_VALIDOS:
            raise ValidationError("Rol inválido. Debe ser 'veterinario' o 'secretaria'")

        if self._usuarios.get_by_email(data.email):
            raise ValidationError("El email ya está en uso")

        nuevo = self._usuarios.add(Usuario(
            nombre=data.nombre,
            email=data.email,
            hashed_password=self._hasher.hash(data.password),
            rol=data.rol,
            activo=1,
            veterinaria_id=veterinaria_id,
        ))
        self._uow.commit()
        return nuevo


class ActualizarUsuarioUseCase:
    def __init__(self, usuario_repo: IUsuarioRepository, hasher: IPasswordHasher, uow: IUnitOfWork):
        self._usuarios = usuario_repo
        self._hasher = hasher
        self._uow = uow

    def execute(self, usuario_id: int, data: UsuarioCreate, veterinaria_id: int) -> Usuario:
        usuario = self._usuarios.get_by_id(usuario_id, veterinaria_id)
        if not usuario:
            raise NotFoundError("Usuario no encontrado")

        usuario.nombre = data.nombre
        usuario.email = data.email
        usuario.rol = data.rol
        if data.password:
            usuario.hashed_password = self._hasher.hash(data.password)

        actualizado = self._usuarios.update(usuario)
        self._uow.commit()
        return actualizado


class DesactivarUsuarioUseCase:
    """Desactiva (baja lógica) un usuario. No puede desactivarse a sí mismo."""

    def __init__(self, usuario_repo: IUsuarioRepository, uow: IUnitOfWork):
        self._usuarios = usuario_repo
        self._uow = uow

    def execute(self, usuario_id: int, usuario_actual_id: int, veterinaria_id: int) -> None:
        if usuario_id == usuario_actual_id:
            raise ValidationError("No puedes eliminar tu propio usuario")

        usuario = self._usuarios.get_by_id(usuario_id, veterinaria_id)
        if not usuario:
            raise NotFoundError("Usuario no encontrado")

        usuario.activo = 0
        self._usuarios.update(usuario)
        self._uow.commit()

