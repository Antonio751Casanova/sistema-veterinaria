from dataclasses import dataclass
from typing import Optional


@dataclass
class Veterinaria:
    """Entidad de dominio: Veterinaria (tenant del sistema)."""
    nombre: str
    telefono: str
    direccion: str
    email: str
    hashed_password: str
    id: Optional[int] = None

