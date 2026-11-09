from dataclasses import dataclass
from typing import Optional

ROL_VETERINARIO = "veterinario"
ROL_SECRETARIA = "secretaria"
ROLES_VALIDOS = (ROL_VETERINARIO, ROL_SECRETARIA)


@dataclass
class Usuario:
    """Entidad de dominio: Usuario (veterinario o secretaria) de una veterinaria."""
    nombre: str
    email: str
    hashed_password: str
    rol: str
    veterinaria_id: int
    activo: int = 1  # 0=inactivo, 1=activo
    id: Optional[int] = None

