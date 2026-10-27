from typing import List

from fastapi import APIRouter, Depends

from app.application.dtos.cliente_dto import ClienteCreate, ClienteResponse, ClienteUpdate
from app.application.dtos.common_dto import MessageResponse
from app.application.use_cases.clientes import (
    ActualizarClienteUseCase, CrearClienteUseCase, EliminarClienteUseCase,
    ListarClientesUseCase, ObtenerClienteUseCase,
)
from app.infrastructure.api.dependencies import (
    CurrentUser, actualizar_cliente_uc, crear_cliente_uc, eliminar_cliente_uc,
    get_current_user, listar_clientes_uc, obtener_cliente_uc,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteResponse)
@router.post("/", response_model=ClienteResponse, include_in_schema=False)
def crear_cliente(
    cliente: ClienteCreate,
    current: CurrentUser = Depends(get_current_user),
    use_case: CrearClienteUseCase = Depends(crear_cliente_uc),
):
    return use_case.execute(cliente, current.veterinaria_id)


@router.get("", response_model=List[ClienteResponse])
@router.get("/", response_model=List[ClienteResponse], include_in_schema=False)
def listar_clientes(
    current: CurrentUser = Depends(get_current_user),
    use_case: ListarClientesUseCase = Depends(listar_clientes_uc),
):
    return use_case.execute(current.veterinaria_id)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: int,
    current: CurrentUser = Depends(get_current_user),
    use_case: ObtenerClienteUseCase = Depends(obtener_cliente_uc),
):
    return use_case.execute(cliente_id, current.veterinaria_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteUpdate,
    current: CurrentUser = Depends(get_current_user),
    use_case: ActualizarClienteUseCase = Depends(actualizar_cliente_uc),
):
    return use_case.execute(cliente_id, datos, current.veterinaria_id)


@router.delete("/{cliente_id}", response_model=MessageResponse)
def eliminar_cliente(
    cliente_id: int,
    current: CurrentUser = Depends(get_current_user),
    use_case: EliminarClienteUseCase = Depends(eliminar_cliente_uc),
):
    use_case.execute(cliente_id, current.veterinaria_id)
    return MessageResponse(success=True, message="Cliente eliminado exitosamente")
