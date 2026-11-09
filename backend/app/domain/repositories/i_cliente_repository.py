from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.cliente import Cliente


class IClienteRepository(ABC):
    """Contrato de persistencia de Clientes. Siempre acotado por veterinaria (multi-tenant)."""

    @abstractmethod
    def add(self, cliente: Cliente) -> Cliente:
        ...

    @abstractmethod
    def get_by_id(self, cliente_id: int, veterinaria_id: int) -> Optional[Cliente]:
        """Devuelve el cliente con `total_mascotas` calculado."""

    @abstractmethod
    def list_by_veterinaria(self, veterinaria_id: int) -> List[Cliente]:
        """Lista clientes (más recientes primero) con `total_mascotas` calculado."""

    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        ...

    @abstractmethod
    def delete(self, cliente_id: int) -> None:
        ...

