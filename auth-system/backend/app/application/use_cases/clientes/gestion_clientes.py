from typing import List

from app.application.dtos.cliente_dto import ClienteCreate, ClienteUpdate
from app.domain.entities.cliente import Cliente
from app.domain.exceptions import NotFoundError
from app.domain.repositories.i_cliente_repository import IClienteRepository
from app.domain.repositories.i_unit_of_work import IUnitOfWork


class CrearClienteUseCase:
    def __init__(self, cliente_repo: IClienteRepository, uow: IUnitOfWork):
        self._clientes = cliente_repo
        self._uow = uow

    def execute(self, data: ClienteCreate, veterinaria_id: int) -> Cliente:
        cliente = self._clientes.add(Cliente(**data.model_dump(), veterinaria_id=veterinaria_id))
        self._uow.commit()
        return cliente


class ListarClientesUseCase:
    def __init__(self, cliente_repo: IClienteRepository):
        self._clientes = cliente_repo

    def execute(self, veterinaria_id: int) -> List[Cliente]:
        return self._clientes.list_by_veterinaria(veterinaria_id)


class ObtenerClienteUseCase:
    def __init__(self, cliente_repo: IClienteRepository):
        self._clientes = cliente_repo

    def execute(self, cliente_id: int, veterinaria_id: int) -> Cliente:
        cliente = self._clientes.get_by_id(cliente_id, veterinaria_id)
        if not cliente:
            raise NotFoundError("Cliente no encontrado")
        return cliente


class ActualizarClienteUseCase:
    def __init__(self, cliente_repo: IClienteRepository, uow: IUnitOfWork):
        self._clientes = cliente_repo
        self._uow = uow

    def execute(self, cliente_id: int, data: ClienteUpdate, veterinaria_id: int) -> Cliente:
        cliente = self._clientes.get_by_id(cliente_id, veterinaria_id)
        if not cliente:
            raise NotFoundError("Cliente no encontrado")

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(cliente, field, value)

        actualizado = self._clientes.update(cliente)
        self._uow.commit()
        return actualizado


class EliminarClienteUseCase:
    def __init__(self, cliente_repo: IClienteRepository, uow: IUnitOfWork):
        self._clientes = cliente_repo
        self._uow = uow

    def execute(self, cliente_id: int, veterinaria_id: int) -> None:
        cliente = self._clientes.get_by_id(cliente_id, veterinaria_id)
        if not cliente:
            raise NotFoundError("Cliente no encontrado")
        self._clientes.delete(cliente_id)
        self._uow.commit()

