from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    """Contrato para hashear y verificar contraseñas."""

    @abstractmethod
    def hash(self, password: str) -> str:
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...

