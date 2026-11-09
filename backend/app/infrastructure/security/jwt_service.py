import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt

from app.domain.services.i_token_service import ITokenService

# Configuración
SECRET_KEY = os.getenv("SECRET_KEY", "veterinaria-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def generate_token() -> str:
    """Generar token aleatorio"""
    return secrets.token_hex(32)


class JwtTokenService(ITokenService):
    """Implementación de ITokenService con PyJWT."""

    def create_token(self, usuario_id: int, veterinaria_id: int, rol: str) -> str:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        payload = {
            "sub": str(usuario_id),
            "vet": str(veterinaria_id),
            "rol": rol,
            "exp": expire,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token if isinstance(token, str) else token.decode("utf-8")

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            clean_token = token.strip().strip('"').strip("'")
            payload = jwt.decode(clean_token, SECRET_KEY, algorithms=[ALGORITHM])
            sub = payload.get("sub")
            vet = payload.get("vet") or sub
            rol = payload.get("rol") or "secretaria"
            if sub is None or vet is None:
                return None
            return {
                "usuario_id": int(sub),
                "veterinaria_id": int(vet),
                "rol": str(rol),
            }
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError, TypeError):
            return None
