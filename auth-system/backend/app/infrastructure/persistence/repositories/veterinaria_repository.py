from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.veterinaria import Veterinaria
from app.domain.repositories.i_veterinaria_repository import IVeterinariaRepository
from app.infrastructure.persistence import models
from app.infrastructure.persistence.mappers import veterinaria_to_entity


class SqlAlchemyVeterinariaRepository(IVeterinariaRepository):
    def __init__(self, session: Session):
        self._db = session

    def get_by_id(self, veterinaria_id: int) -> Optional[Veterinaria]:
        m = self._db.query(models.Veterinaria).filter(models.Veterinaria.id == veterinaria_id).first()
        return veterinaria_to_entity(m) if m else None

    def get_by_email(self, email: str) -> Optional[Veterinaria]:
        m = self._db.query(models.Veterinaria).filter(models.Veterinaria.email == email).first()
        return veterinaria_to_entity(m) if m else None

    def add(self, veterinaria: Veterinaria) -> Veterinaria:
        m = models.Veterinaria(
            nombre=veterinaria.nombre, telefono=veterinaria.telefono,
            direccion=veterinaria.direccion, email=veterinaria.email,
            hashed_password=veterinaria.hashed_password,
        )
        self._db.add(m)
        self._db.flush()
        return veterinaria_to_entity(m)

