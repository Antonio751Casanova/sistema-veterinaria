from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClienteBase(BaseModel):
    """Schema base de cliente (solo dueño)"""
    nombre: str
    telefono: str
    email: Optional[str] = None
    direccion: Optional[str] = None


class ClienteCreate(ClienteBase):
    """Schema para crear cliente"""
    pass


class ClienteUpdate(BaseModel):
    """Schema para actualizar cliente"""
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema de respuesta de cliente"""
    id: int
    veterinaria_id: int
    fecha_creacion: datetime
    total_mascotas: int = 0

    class Config:
        from_attributes = True

