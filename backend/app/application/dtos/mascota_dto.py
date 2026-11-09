from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MascotaBase(BaseModel):
    """Schema base de mascota"""
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    notas: Optional[str] = None


class MascotaCreate(MascotaBase):
    """Schema para crear mascota"""
    pass


class MascotaUpdate(BaseModel):
    """Schema para actualizar mascota"""
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[str] = None
    peso: Optional[str] = None
    notas: Optional[str] = None


class MascotaResponse(MascotaBase):
    """Schema de respuesta de mascota"""
    id: int
    cliente_id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class MascotaConDuenoResponse(MascotaBase):
    """Schema de respuesta de mascota con datos del dueño"""
    id: int
    cliente_id: int
    fecha_creacion: datetime
    nombre_dueno: str
    telefono_dueno: str

    class Config:
        from_attributes = True

