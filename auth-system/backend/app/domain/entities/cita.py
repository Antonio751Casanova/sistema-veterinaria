from dataclasses import dataclass
from datetime import datetime
from typing import Optional

ESTADOS_CITA = ("pendiente", "confirmado", "rechazado", "en_espera", "completado")


@dataclass
class Cita:
    """Entidad de dominio: Cita (preparada para el Avance 2; aún sin casos de uso)."""
    fecha_hora: datetime
    tipo_atencion: str
    mascota_id: int
    descripcion: Optional[str] = None
    tratamiento: Optional[str] = None
    medicamento: Optional[str] = None
    costo: Optional[str] = None
    duracion_minutos: int = 60
    estado: str = "pendiente"
    confirmation_token: Optional[str] = None
    recordatorio_whatsapp_enviado: int = 0
    recordatorio_email_enviado: int = 0
    veterinario_asignado_id: Optional[int] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None

