from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.common_dto import MessageResponse
from app.application.dtos.notificacion_dto import NotificacionResponse
from app.infrastructure.persistence.models import (
    Veterinaria, Usuario, Cliente, Mascota, Bitacora, Cita, ListaEspera, Notificacion
)
from app.infrastructure.api.dependencies import CurrentUser, get_current_user, require_role, get_db

router = APIRouter()

@router.get("/notificaciones", response_model=List[NotificacionResponse], tags=["Notificaciones"])
def listar_notificaciones(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Notificacion).filter(
        Notificacion.veterinaria_id == current.veterinaria_id
    )
    if current.rol == "veterinario":
        query = query.filter(
            Notificacion.destinatario_usuario_id == current.usuario_id
        )
    return query.order_by(Notificacion.fecha_creacion.desc()).all()


@router.get("/notificaciones/no-leidas", response_model=List[NotificacionResponse], tags=["Notificaciones"])
def listar_notificaciones_no_leidas(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Notificacion).filter(
        Notificacion.veterinaria_id == current.veterinaria_id,
        Notificacion.leida == 0
    )
    if current.rol == "veterinario":
        query = query.filter(
            Notificacion.destinatario_usuario_id == current.usuario_id
        )
    return query.order_by(Notificacion.fecha_creacion.desc()).all()


@router.put("/notificaciones/{notificacion_id}/leer", response_model=NotificacionResponse, tags=["Notificaciones"])
def marcar_notificacion_leida(
    notificacion_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notificacion = db.query(Notificacion).filter(
        Notificacion.id == notificacion_id,
        Notificacion.veterinaria_id == current.veterinaria_id
    ).first()
    if not notificacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")

    notificacion.leida = 1
    db.commit()
    db.refresh(notificacion)
    return notificacion


@router.delete("/notificaciones/{notificacion_id}", response_model=MessageResponse, tags=["Notificaciones"])
def eliminar_notificacion(
    notificacion_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notificacion = db.query(Notificacion).filter(
        Notificacion.id == notificacion_id,
        Notificacion.veterinaria_id == current.veterinaria_id
    ).first()
    if not notificacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")

    db.delete(notificacion)
    db.commit()
    return MessageResponse(success=True, message="Notificación eliminada exitosamente")
