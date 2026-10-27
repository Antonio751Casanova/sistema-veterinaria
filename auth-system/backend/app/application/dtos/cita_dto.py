from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CitaBase(BaseModel):
    """Schema base de cita"""
    fecha_hora: datetime
    tipo_atencion: str
    descripcion: Optional[str] = None
    tratamiento: Optional[str] = None
    medicamento: Optional[str] = None
    costo: Optional[str] = None
    estado: Optional[str] = "pendiente"
    duracion_minutos: Optional[int] = 60


class CitaCreate(CitaBase):
    """Schema para crear cita"""
    mascota_id: int
    veterinario_asignado_id: Optional[int] = None


class CitaUpdate(BaseModel):
    """Schema para actualizar cita"""
    fecha_hora: Optional[datetime] = None
    tipo_atencion: Optional[str] = None
    descripcion: Optional[str] = None
    tratamiento: Optional[str] = None
    medicamento: Optional[str] = None
    costo: Optional[str] = None
    estado: Optional[str] = None
    veterinario_asignado_id: Optional[int] = None
    duracion_minutos: Optional[int] = None


class CitaResponse(CitaBase):
    """Schema de respuesta de cita"""
    id: int
    mascota_id: int
    recordatorio_whatsapp_enviado: int
    recordatorio_email_enviado: int
    fecha_creacion: datetime
    confirmation_token: Optional[str] = None

    class Config:
        from_attributes = True


class CitaConDetallesResponse(CitaBase):
    """Schema de respuesta de cita con datos de mascota y cliente"""
    id: int
    mascota_id: int
    recordatorio_whatsapp_enviado: int
    recordatorio_email_enviado: int
    fecha_creacion: datetime
    nombre_mascota: str
    especie_mascota: str
    nombre_cliente: str
    telefono_cliente: str
    email_cliente: Optional[str] = None
    confirmation_token: Optional[str] = None
    veterinario_asignado_id: Optional[int] = None
    nombre_veterinario_asignado: Optional[str] = None

    class Config:
        from_attributes = True


class CitaConfirmacionPublicResponse(BaseModel):
    """Schema público para confirmación/rechazo por el cliente (sin JWT)"""
    id: int
    estado: str
    fecha_hora: datetime
    tipo_atencion: str
    nombre_mascota: str
    nombre_cliente: str
    message: str

    class Config:
        from_attributes = True

