from typing import List

from fastapi import APIRouter, Depends

from app.application.dtos.common_dto import MessageResponse
from app.application.dtos.mascota_dto import (
    MascotaConDuenoResponse, MascotaCreate, MascotaResponse, MascotaUpdate,
)
from app.application.use_cases.mascotas import (
    ActualizarMascotaUseCase, CrearMascotaUseCase, EliminarMascotaUseCase,
    ListarMascotasClienteUseCase, ListarTodasMascotasUseCase, ObtenerMascotaUseCase,
)
from app.infrastructure.api.dependencies import (
    CurrentUser, actualizar_mascota_uc, crear_mascota_uc, eliminar_mascota_uc,
    get_current_user, listar_mascotas_cliente_uc, listar_todas_mascotas_uc,
    obtener_mascota_uc,
)

router = APIRouter(tags=["Mascotas"])


@router.post("/clientes/{cliente_id}/mascotas", response_model=MascotaResponse)
def crear_mascota(
    cliente_id: int,
    mascota: MascotaCreate,
    current: CurrentUser = Depends(get_current_user),
    use_case: CrearMascotaUseCase = Depends(crear_mascota_uc),
):
    return use_case.execute(cliente_id, mascota, current.veterinaria_id)


@router.get("/clientes/{cliente_id}/mascotas", response_model=List[MascotaResponse])
def listar_mascotas_cliente(
    cliente_id: int,
    current: CurrentUser = Depends(get_current_user),
    use_case: ListarMascotasClienteUseCase = Depends(listar_mascotas_cliente_uc),
):
    return use_case.execute(cliente_id, current.veterinaria_id)


@router.get("/mascotas", response_model=List[MascotaConDuenoResponse])
def listar_todas_mascotas(
    current: CurrentUser = Depends(get_current_user),
    use_case: ListarTodasMascotasUseCase = Depends(listar_todas_mascotas_uc),
):
    return use_case.execute(current.veterinaria_id)


@router.get("/mascotas/{mascota_id}", response_model=MascotaConDuenoResponse)
def obtener_mascota(
    mascota_id: int,
    current: CurrentUser = Depends(get_current_user),
    use_case: ObtenerMascotaUseCase = Depends(obtener_mascota_uc),
):
    return use_case.execute(mascota_id, current.veterinaria_id)


@router.put("/mascotas/{mascota_id}", response_model=MascotaResponse)
def actualizar_mascota(
    mascota_id: int,
    datos: MascotaUpdate,
    current: CurrentUser = Depends(get_current_user),
    use_case: ActualizarMascotaUseCase = Depends(actualizar_mascota_uc),
):
    return use_case.execute(mascota_id, datos, current.veterinaria_id)


@router.delete("/mascotas/{mascota_id}", response_model=MessageResponse)
def eliminar_mascota(
    mascota_id: int,
    current: CurrentUser = Depends(get_current_user),
    use_case: EliminarMascotaUseCase = Depends(eliminar_mascota_uc),
):
    use_case.execute(mascota_id, current.veterinaria_id)
    return MessageResponse(success=True, message="Mascota eliminada exitosamente")

