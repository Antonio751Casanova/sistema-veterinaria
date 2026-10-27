from typing import List

from app.application.dtos.mascota_dto import MascotaCreate, MascotaUpdate
from app.domain.entities.mascota import Mascota
from app.domain.exceptions import NotFoundError
from app.domain.repositories.i_cliente_repository import IClienteRepository
from app.domain.repositories.i_mascota_repository import IMascotaRepository
from app.domain.repositories.i_unit_of_work import IUnitOfWork


def _obtener_o_fallar(mascotas: IMascotaRepository, mascota_id: int, veterinaria_id: int) -> Mascota:
    mascota = mascotas.get_by_id(mascota_id, veterinaria_id)
    if not mascota:
        raise NotFoundError("Mascota no encontrada")
    return mascota


class CrearMascotaUseCase:
    def __init__(self, mascota_repo: IMascotaRepository, cliente_repo: IClienteRepository, uow: IUnitOfWork):
        self._mascotas = mascota_repo
        self._clientes = cliente_repo
        self._uow = uow

    def execute(self, cliente_id: int, data: MascotaCreate, veterinaria_id: int) -> Mascota:
        if not self._clientes.get_by_id(cliente_id, veterinaria_id):
            raise NotFoundError("Cliente no encontrado")
        mascota = self._mascotas.add(Mascota(**data.model_dump(), cliente_id=cliente_id))
        self._uow.commit()
        return mascota


class ListarMascotasClienteUseCase:
    def __init__(self, mascota_repo: IMascotaRepository, cliente_repo: IClienteRepository):
        self._mascotas = mascota_repo
        self._clientes = cliente_repo

    def execute(self, cliente_id: int, veterinaria_id: int) -> List[Mascota]:
        if not self._clientes.get_by_id(cliente_id, veterinaria_id):
            raise NotFoundError("Cliente no encontrado")
        return self._mascotas.list_by_cliente(cliente_id)


class ListarTodasMascotasUseCase:
    def __init__(self, mascota_repo: IMascotaRepository):
        self._mascotas = mascota_repo

    def execute(self, veterinaria_id: int) -> List[Mascota]:
        return self._mascotas.list_by_veterinaria(veterinaria_id)


class ObtenerMascotaUseCase:
    def __init__(self, mascota_repo: IMascotaRepository):
        self._mascotas = mascota_repo

    def execute(self, mascota_id: int, veterinaria_id: int) -> Mascota:
        return _obtener_o_fallar(self._mascotas, mascota_id, veterinaria_id)


class ActualizarMascotaUseCase:
    def __init__(self, mascota_repo: IMascotaRepository, uow: IUnitOfWork):
        self._mascotas = mascota_repo
        self._uow = uow

    def execute(self, mascota_id: int, data: MascotaUpdate, veterinaria_id: int) -> Mascota:
        mascota = _obtener_o_fallar(self._mascotas, mascota_id, veterinaria_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(mascota, field, value)

        actualizada = self._mascotas.update(mascota)
        self._uow.commit()
        return actualizada


class EliminarMascotaUseCase:
    def __init__(self, mascota_repo: IMascotaRepository, uow: IUnitOfWork):
        self._mascotas = mascota_repo
        self._uow = uow

    def execute(self, mascota_id: int, veterinaria_id: int) -> None:
        _obtener_o_fallar(self._mascotas, mascota_id, veterinaria_id)
        self._mascotas.delete(mascota_id)
        self._uow.commit()

