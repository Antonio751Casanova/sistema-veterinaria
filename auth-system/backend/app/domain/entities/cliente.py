from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    """Entidad de dominio: Cliente (dueño de mascotas)."""
    nombre: str
    telefono: str
    veterinaria_id: int
    email: Optional[str] = None
    direccion: Optional[str] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    total_mascotas: int = 0  # dato calculado por el repositorio

