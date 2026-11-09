from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.repositories.i_usuario_repository import IUsuarioRepository
from app.infrastructure.persistence import models
from app.infrastructure.persistence.mappers import usuario_to_entity


class SqlAlchemyUsuarioRepository(IUsuarioRepository):
    def __init__(self, session: Session):
        self._db = session

    def get_active_by_id(self, usuario_id: int) -> Optional[Usuario]:
        m = self._db.query(models.Usuario).filter(
            models.Usuario.id == usuario_id, models.Usuario.activo == 1
        ).first()
        return usuario_to_entity(m) if m else None

    def get_by_id(self, usuario_id: int, veterinaria_id: int) -> Optional[Usuario]:
        m = self._db.query(models.Usuario).filter(
            models.Usuario.id == usuario_id,
            models.Usuario.veterinaria_id == veterinaria_id,
        ).first()
        return usuario_to_entity(m) if m else None

    def get_by_email(self, email: str) -> Optional[Usuario]:
        m = self._db.query(models.Usuario).filter(models.Usuario.email == email).first()
        return usuario_to_entity(m) if m else None

    def get_active_by_email(self, email: str) -> Optional[Usuario]:
        m = self._db.query(models.Usuario).filter(
            models.Usuario.email == email, models.Usuario.activo == 1
        ).first()
        return usuario_to_entity(m) if m else None

    def list_by_veterinaria(self, veterinaria_id: int) -> List[Usuario]:
        rows = self._db.query(models.Usuario).filter(
            models.Usuario.veterinaria_id == veterinaria_id
        ).order_by(models.Usuario.id.asc()).all()
        return [usuario_to_entity(m) for m in rows]

    def add(self, usuario: Usuario) -> Usuario:
        m = models.Usuario(
            nombre=usuario.nombre, email=usuario.email,
            hashed_password=usuario.hashed_password, rol=usuario.rol,
            activo=usuario.activo, veterinaria_id=usuario.veterinaria_id,
        )
        self._db.add(m)
        self._db.flush()
        return usuario_to_entity(m)

    def update(self, usuario: Usuario) -> Usuario:
        m = self._db.query(models.Usuario).filter(models.Usuario.id == usuario.id).one()
        m.nombre = usuario.nombre
        m.email = usuario.email
        m.hashed_password = usuario.hashed_password
        m.rol = usuario.rol
        m.activo = usuario.activo
        self._db.flush()
        return usuario_to_entity(m)

