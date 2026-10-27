from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ListaEsperaBase(BaseModel):
    """Schema base de lista de espera"""
    tipo_atencion: str
    duracion_minutos: Optional[int] = 60
    prioridad: Optional[int] = 0
    hora_inicio_preferida: Optional[int] = None
    hora_fin_preferida: Optional[int] = None
    notas: Optional[str] = None
    preferencia_veterinario_id: Optional[int] = None


class ListaEsperaCreate(ListaEsperaBase):
    """Schema para crear una entrada de lista de espera"""
    mascota_id: int


class ListaEsperaUpdate(BaseModel):
    """Schema para actualizar una entrada de lista de espera"""
    tipo_atencion: Optional[str] = None
    duracion_minutos: Optional[int] = None
    prioridad: Optional[int] = None
    hora_inicio_preferida: Optional[int] = None
    hora_fin_preferida: Optional[int] = None
    notas: Optional[str] = None
    preferencia_veterinario_id: Optional[int] = None
    estado: Optional[str] = None


class ListaEsperaResponse(ListaEsperaBase):
    """Schema de respuesta de lista de espera"""
    id: int
    mascota_id: int
    veterinaria_id: int
    estado: str
    fecha_creacion: datetime
    nombre_mascota: str
    especie_mascota: str
    nombre_cliente: str
    telefono_cliente: str
    preferencia_veterinario_nombre: Optional[str] = None

    class Config:
        from_attributes = True

