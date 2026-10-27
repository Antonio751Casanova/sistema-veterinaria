from typing import List

from fastapi import APIRouter, Depends

from app.application.dtos.common_dto import MessageResponse
from app.application.dtos.usuario_dto import UsuarioCreate, UsuarioResponse
from app.application.use_cases.usuarios import (
    ActualizarUsuarioUseCase, CrearUsuarioUseCase, DesactivarUsuarioUseCase,
    ListarUsuariosUseCase,
)
from app.infrastructure.api.dependencies import (
    CurrentUser, actualizar_usuario_uc, crear_usuario_uc, desactivar_usuario_uc,
    listar_usuarios_uc, require_role,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios(
    current: CurrentUser = Depends(require_role("secretaria")),
    use_case: ListarUsuariosUseCase = Depends(listar_usuarios_uc),
):
    """Listar todos los usuarios de la veterinaria (solo secretaria)"""
    return use_case.execute(current.veterinaria_id)


@router.post("", response_model=UsuarioResponse)
def crear_usuario(
    data: UsuarioCreate,
    current: CurrentUser = Depends(require_role("secretaria")),
    use_case: CrearUsuarioUseCase = Depends(crear_usuario_uc),
):
    """Crear nuevo usuario bajo la veterinaria (solo secretaria)"""
    return use_case.execute(data, current.veterinaria_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioCreate,
    current: CurrentUser = Depends(require_role("secretaria")),
    use_case: ActualizarUsuarioUseCase = Depends(actualizar_usuario_uc),
):
    """Actualizar usuario (solo secretaria)"""
    return use_case.execute(usuario_id, data, current.veterinaria_id)


@router.delete("/{usuario_id}", response_model=MessageResponse)
def eliminar_usuario(
    usuario_id: int,
    current: CurrentUser = Depends(require_role("secretaria")),
    use_case: DesactivarUsuarioUseCase = Depends(desactivar_usuario_uc),
):
    """Eliminar/desactivar usuario (solo secretaria, no puede eliminarse a sí mismo)"""
    use_case.execute(usuario_id, current.usuario_id, current.veterinaria_id)
    return MessageResponse(success=True, message="Usuario desactivado exitosamente")

