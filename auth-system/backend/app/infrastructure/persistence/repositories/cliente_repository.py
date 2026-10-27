from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.cliente import Cliente
from app.domain.repositories.i_cliente_repository import IClienteRepository
from app.infrastructure.persistence import models
from app.infrastructure.persistence.mappers import cliente_to_entity


class SqlAlchemyClienteRepository(IClienteRepository):
    def __init__(self, session: Session):
        self._db = session

    def _count_mascotas(self, cliente_id: int) -> int:
        return self._db.query(models.Mascota).filter(models.Mascota.cliente_id == cliente_id).count()

    def add(self, cliente: Cliente) -> Cliente:
        m = models.Cliente(
            nombre=cliente.nombre, telefono=cliente.telefono, email=cliente.email,
            direccion=cliente.direccion, veterinaria_id=cliente.veterinaria_id,
        )
        self._db.add(m)
        self._db.flush()
        return cliente_to_entity(m)

    def get_by_id(self, cliente_id: int, veterinaria_id: int) -> Optional[Cliente]:
        m = self._db.query(models.Cliente).filter(
            models.Cliente.id == cliente_id,
            models.Cliente.veterinaria_id == veterinaria_id,
        ).first()
        return cliente_to_entity(m, self._count_mascotas(m.id)) if m else None

    def list_by_veterinaria(self, veterinaria_id: int) -> List[Cliente]:
        rows = self._db.query(models.Cliente).filter(
            models.Cliente.veterinaria_id == veterinaria_id
        ).order_by(models.Cliente.id.desc()).all()
        return [cliente_to_entity(m, self._count_mascotas(m.id)) for m in rows]

    def update(self, cliente: Cliente) -> Cliente:
        m = self._db.query(models.Cliente).filter(models.Cliente.id == cliente.id).one()
        m.nombre = cliente.nombre
        m.telefono = cliente.telefono
        m.email = cliente.email
        m.direccion = cliente.direccion
        self._db.flush()
        return cliente_to_entity(m, self._count_mascotas(m.id))

    def delete(self, cliente_id: int) -> None:
        m = self._db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if m:
            self._db.delete(m)
            self._db.flush()

