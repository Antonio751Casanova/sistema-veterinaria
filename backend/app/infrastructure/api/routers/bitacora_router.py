from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.bitacora_dto import BitacoraCreate, BitacoraResponse
from app.application.dtos.common_dto import MessageResponse
from app.infrastructure.persistence.models import (
    Veterinaria, Usuario, Cliente, Mascota, Bitacora, Cita, ListaEspera, Notificacion
)
from app.infrastructure.api.dependencies import CurrentUser, get_current_user, require_role, get_db

router = APIRouter()

@router.post("/mascotas/{mascota_id}/bitacora", response_model=BitacoraResponse, tags=["Bitácora"])
def crear_entrada_bitacora(
    mascota_id: int,
    entrada: BitacoraCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).join(Cliente).filter(
        Mascota.id == mascota_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")

    nueva_entrada = Bitacora(**entrada.model_dump(), mascota_id=mascota_id)
    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada


@router.get("/mascotas/{mascota_id}/bitacora", response_model=List[BitacoraResponse], tags=["Bitácora"])
def listar_bitacora(
    mascota_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).join(Cliente).filter(
        Mascota.id == mascota_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")

    return db.query(Bitacora).filter(
        Bitacora.mascota_id == mascota_id
    ).order_by(Bitacora.fecha.desc()).all()


@router.delete("/mascotas/{mascota_id}/bitacora/{entrada_id}", response_model=MessageResponse, tags=["Bitácora"])
def eliminar_entrada_bitacora(
    mascota_id: int,
    entrada_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).join(Cliente).filter(
        Mascota.id == mascota_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")

    entrada = db.query(Bitacora).filter(
        Bitacora.id == entrada_id,
        Bitacora.mascota_id == mascota_id
    ).first()
    if not entrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrada de bitácora no encontrada")

    db.delete(entrada)
    db.commit()
    return MessageResponse(success=True, message="Entrada de bitácora eliminada exitosamente")
