from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Mascota:
    """Entidad de dominio: Mascota perteneciente a un Cliente."""
    nombre: str
    especie: str
    cliente_id: int
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    notas: Optional[str] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    # Datos de solo lectura del dueño, poblados por el repositorio en consultas con dueño
    nombre_dueno: Optional[str] = None
    telefono_dueno: Optional[str] = None

