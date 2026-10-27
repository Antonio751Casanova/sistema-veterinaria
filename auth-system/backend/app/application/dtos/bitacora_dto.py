from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BitacoraBase(BaseModel):
    """Schema base de bitácora"""
    tipo: str
    descripcion: str
    tratamiento: Optional[str] = None
    medicamentos: Optional[str] = None
    costo: Optional[str] = None
    proxima_cita: Optional[datetime] = None


class BitacoraCreate(BitacoraBase):
    """Schema para crear entrada de bitácora"""
    pass


class BitacoraResponse(BitacoraBase):
    """Schema de respuesta de bitácora"""
    id: int
    fecha: datetime
    mascota_id: int

    class Config:
        from_attributes = True

