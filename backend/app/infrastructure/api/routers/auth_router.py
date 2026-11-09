from fastapi import APIRouter, Depends

from app.application.dtos.auth_dto import (
    LoginResponse, VeterinariaCreate, VeterinariaLogin, VeterinariaResponse,
)
from app.application.use_cases.auth import LoginUseCase, RegistrarVeterinariaUseCase
from app.infrastructure.api.dependencies import (
    CurrentUser, get_current_user, login_uc, registrar_veterinaria_uc,
)

router = APIRouter(tags=["Auth"])


@router.post("/veterinarias/registro", response_model=VeterinariaResponse)
def registrar_veterinaria(
    data: VeterinariaCreate,
    use_case: RegistrarVeterinariaUseCase = Depends(registrar_veterinaria_uc),
):
    """Registrar una nueva veterinaria y su primer usuario (secretaria)"""
    return use_case.execute(data)


@router.post("/veterinarias/login", response_model=LoginResponse)
def login_veterinaria(
    credentials: VeterinariaLogin,
    use_case: LoginUseCase = Depends(login_uc),
):
    """Login unificado por email/contraseña de usuario"""
    return use_case.execute(credentials)


@router.get("/veterinarias/me", response_model=VeterinariaResponse)
def obtener_veterinaria_actual(current: CurrentUser = Depends(get_current_user)):
    return current.veterinaria

