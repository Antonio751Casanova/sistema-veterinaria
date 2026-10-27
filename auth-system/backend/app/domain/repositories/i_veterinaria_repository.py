from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.veterinaria import Veterinaria


class IVeterinariaRepository(ABC):
    """Contrato de persistencia de Veterinarias (interfaz segregada)."""

    @abstractmethod
    def get_by_id(self, veterinaria_id: int) -> Optional[Veterinaria]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Veterinaria]:
        ...

    @abstractmethod
    def add(self, veterinaria: Veterinaria) -> Veterinaria:
        """Agrega la veterinaria (asigna id). No confirma la transacción."""

