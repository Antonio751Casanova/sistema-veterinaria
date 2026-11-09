from abc import ABC, abstractmethod
from typing import Optional


class ITokenService(ABC):
    """Contrato para emitir y validar tokens de acceso."""

    @abstractmethod
    def create_token(self, usuario_id: int, veterinaria_id: int, rol: str) -> str:
        ...

    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        """Devuelve {'usuario_id', 'veterinaria_id', 'rol'} o None si es inválido/expirado."""

