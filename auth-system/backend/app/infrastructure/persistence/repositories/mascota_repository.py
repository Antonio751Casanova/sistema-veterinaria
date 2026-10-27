from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.mascota import Mascota
from app.domain.repositories.i_mascota_repository import IMascotaRepository
from app.infrastructure.persistence import models
from app.infrastructure.persistence.mappers import mascota_to_entity


class SqlAlchemyMascotaRepository(IMascotaRepository):
    def __init__(self, session: Session):
        self._db = session

    def add(self, mascota: Mascota) -> Mascota:
        m = models.Mascota(
            nombre=mascota.nombre, especie=mascota.especie, raza=mascota.raza,
            edad=mascota.edad, peso=mascota.peso, notas=mascota.notas,
            cliente_id=mascota.cliente_id,
        )
        self._db.add(m)
        self._db.flush()
        return mascota_to_entity(m)

    def get_by_id(self, mascota_id: int, veterinaria_id: int) -> Optional[Mascota]:
        m = self._db.query(models.Mascota).join(models.Cliente).filter(
            models.Mascota.id == mascota_id,
            models.Cliente.veterinaria_id == veterinaria_id,
        ).first()
        return mascota_to_entity(m, con_dueno=True) if m else None

    def list_by_cliente(self, cliente_id: int) -> List[Mascota]:
        rows = self._db.query(models.Mascota).filter(
            models.Mascota.cliente_id == cliente_id
        ).order_by(models.Mascota.id.desc()).all()
        return [mascota_to_entity(m) for m in rows]

    def list_by_veterinaria(self, veterinaria_id: int) -> List[Mascota]:
        rows = self._db.query(models.Mascota).join(models.Cliente).filter(
            models.Cliente.veterinaria_id == veterinaria_id
        ).order_by(models.Mascota.id.desc()).all()
        return [mascota_to_entity(m, con_dueno=True) for m in rows]

    def update(self, mascota: Mascota) -> Mascota:
        m = self._db.query(models.Mascota).filter(models.Mascota.id == mascota.id).one()
        m.nombre = mascota.nombre
        m.especie = mascota.especie
        m.raza = mascota.raza
        m.edad = mascota.edad
        m.peso = mascota.peso
        m.notas = mascota.notas
        self._db.flush()
        return mascota_to_entity(m)

    def delete(self, mascota_id: int) -> None:
        m = self._db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
        if m:
            self._db.delete(m)
            self._db.flush()

