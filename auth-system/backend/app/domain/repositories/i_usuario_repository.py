from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.usuario import Usuario


class IUsuarioRepository(ABC):
    """Contrato de persistencia de Usuarios."""

    @abstractmethod
    def get_active_by_id(self, usuario_id: int) -> Optional[Usuario]:
        ...

    @abstractmethod
    def get_by_id(self, usuario_id: int, veterinaria_id: int) -> Optional[Usuario]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def get_active_by_email(self, email: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def list_by_veterinaria(self, veterinaria_id: int) -> List[Usuario]:
        ...

    @abstractmethod
    def add(self, usuario: Usuario) -> Usuario:
        """Agrega el usuario (asigna id). No confirma la transacción."""

    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """Persiste los cambios del usuario. No confirma la transacción."""

