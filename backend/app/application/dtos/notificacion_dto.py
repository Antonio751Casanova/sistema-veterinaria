from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificacionBase(BaseModel):
    """Schema base de notificación"""
    tipo: str
    mensaje: str


class NotificacionCreate(NotificacionBase):
    """Schema para crear notificación"""
    cita_id: Optional[int] = None
    destinatario_usuario_id: Optional[int] = None


class NotificacionResponse(NotificacionBase):
    """Schema de respuesta de notificación"""
    id: int
    leida: int
    fecha_creacion: datetime
    cita_id: Optional[int] = None
    destinatario_usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

