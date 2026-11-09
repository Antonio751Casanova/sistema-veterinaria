from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.mascota import Mascota


class IMascotaRepository(ABC):
    """Contrato de persistencia de Mascotas. Las consultas por veterinaria validan pertenencia vía el dueño."""

    @abstractmethod
    def add(self, mascota: Mascota) -> Mascota:
        ...

    @abstractmethod
    def get_by_id(self, mascota_id: int, veterinaria_id: int) -> Optional[Mascota]:
        """Devuelve la mascota con datos del dueño (`nombre_dueno`, `telefono_dueno`)."""

    @abstractmethod
    def list_by_cliente(self, cliente_id: int) -> List[Mascota]:
        ...

    @abstractmethod
    def list_by_veterinaria(self, veterinaria_id: int) -> List[Mascota]:
        """Lista mascotas (más recientes primero) con datos del dueño."""

    @abstractmethod
    def update(self, mascota: Mascota) -> Mascota:
        ...

    @abstractmethod
    def delete(self, mascota_id: int) -> None:
        ...

