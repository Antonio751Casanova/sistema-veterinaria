from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """Contrato para confirmar/revertir una transacción de negocio."""

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

