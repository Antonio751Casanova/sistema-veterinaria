from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Schema para respuesta genérica"""
    success: bool
    message: str

