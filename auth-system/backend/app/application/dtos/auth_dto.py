from typing import Optional

from pydantic import BaseModel

from .usuario_dto import UsuarioResponse


class VeterinariaCreate(BaseModel):
    """Schema para registrar una veterinaria"""
    nombre: str
    telefono: str
    direccion: str
    email: str
    password: str


class VeterinariaLogin(BaseModel):
    """Schema para login de veterinaria"""
    email: str
    password: str


class VeterinariaResponse(BaseModel):
    """Schema de respuesta de veterinaria"""
    id: int
    nombre: str
    telefono: str
    direccion: str
    email: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Schema de respuesta de login"""
    success: bool
    message: str
    token: Optional[str] = None
    veterinaria: Optional[VeterinariaResponse] = None
    usuario: Optional[UsuarioResponse] = None

