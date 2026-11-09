from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    """Schema para crear un usuario"""
    nombre: str
    email: str
    password: str
    rol: str  # "veterinario" | "secretaria"


class UsuarioResponse(BaseModel):
    """Schema de respuesta de usuario"""
    id: int
    nombre: str
    email: str
    rol: str
    activo: int = 1

    class Config:
        from_attributes = True

