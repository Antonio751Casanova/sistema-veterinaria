from datetime import datetime, timedelta
from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.cita_dto import (
    CitaCreate, CitaUpdate, CitaResponse, CitaConDetallesResponse,
    CitaConfirmacionPublicResponse,
)
from app.application.dtos.common_dto import MessageResponse
from app.infrastructure.persistence.models import (
    Veterinaria, Usuario, Cliente, Mascota, Bitacora, Cita, ListaEspera, Notificacion
)
from app.infrastructure.api.dependencies import CurrentUser, get_current_user, require_role, get_db
from app.infrastructure.api.cita_helpers import (
    _build_cita_response, _generar_sugerencias_lista_espera, _has_pet_datetime_conflict,
)

router = APIRouter()

@router.post("/citas", response_model=CitaResponse, tags=["Citas"])
def crear_cita(
    data: CitaCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva cita. Secretaria debe especificar veterinario_asignado_id."""
    if current.rol == "secretaria" and not data.veterinario_asignado_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La secretaria debe seleccionar un veterinario al crear una cita"
        )

    duracion = int(data.duracion_minutos or 60)
    if duracion < 15 or duracion > 480:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración de la cita debe estar entre 15 y 480 minutos"
        )

    mascota = db.query(Mascota).join(Cliente).filter(
        Mascota.id == data.mascota_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")

    if _has_pet_datetime_conflict(
        db=db,
        veterinaria_id=current.veterinaria_id,
        mascota_id=data.mascota_id,
        fecha_hora=data.fecha_hora,
        duracion_minutos=duracion
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La mascota ya tiene una cita activa que se empalma con ese horario"
        )

    # Validar que el veterinario asignado pertenece a la misma veterinaria
    if data.veterinario_asignado_id:
        vet_asignado = db.query(Usuario).filter(
            Usuario.id == data.veterinario_asignado_id,
            Usuario.veterinaria_id == current.veterinaria_id,
            Usuario.rol == "veterinario"
        ).first()
        if not vet_asignado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Veterinario asignado no válido"
            )

    nueva_cita = Cita(
        fecha_hora=data.fecha_hora,
        tipo_atencion=data.tipo_atencion,
        descripcion=data.descripcion,
        tratamiento=data.tratamiento,
        medicamento=data.medicamento,
        costo=data.costo,
        duracion_minutos=duracion,
        estado=data.estado or "pendiente",
        mascota_id=data.mascota_id,
        veterinario_asignado_id=data.veterinario_asignado_id,
        confirmation_token=str(uuid.uuid4())
    )
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    # Notificación de recordatorio
    fecha_recordatorio = data.fecha_hora - timedelta(days=1)
    if fecha_recordatorio > datetime.now():
        notificacion = Notificacion(
            tipo="recordatorio_cita",
            mensaje=f"Recordar enviar recordatorio de cita para {mascota.nombre} programada para {data.fecha_hora.strftime('%d/%m/%Y %H:%M')}",
            cita_id=nueva_cita.id,
            veterinaria_id=current.veterinaria_id
        )
        db.add(notificacion)

    # Notificación de asignación al veterinario
    if nueva_cita.veterinario_asignado_id:
        vet = db.query(Usuario).filter(Usuario.id == nueva_cita.veterinario_asignado_id).first()
        if vet:
            asignacion = Notificacion(
                tipo="cita_asignada",
                mensaje=(
                    f"Nueva cita asignada: {mascota.nombre} ({mascota.cliente.nombre}) - "
                    f"{data.fecha_hora.strftime('%d/%m/%Y %H:%M')} · {data.tipo_atencion}"
                ),
                cita_id=nueva_cita.id,
                veterinaria_id=current.veterinaria_id,
                destinatario_usuario_id=vet.id
            )
            db.add(asignacion)

    db.commit()

    return nueva_cita


@router.get("/citas", response_model=List[CitaConDetallesResponse], tags=["Citas"])
def listar_citas(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Secretaria: ve todas las citas de la veterinaria.
    Veterinario: solo sus citas futuras asignadas.
    """
    query = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id
    )

    if current.rol == "veterinario":
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(
            Cita.veterinario_asignado_id == current.usuario_id,
            Cita.fecha_hora >= today_start
        )

    citas = query.order_by(Cita.fecha_hora.asc()).all()
    return [_build_cita_response(c) for c in citas]


@router.get("/citas/confirmar", response_model=CitaConfirmacionPublicResponse, tags=["Citas Públicas"])
def confirmar_cita_publica(token: str, db: Session = Depends(get_db)):
    """Confirmar una cita mediante token público."""
    cita = db.query(Cita).filter(Cita.confirmation_token == token).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enlace de confirmación inválido o expirado")

    if cita.fecha_hora < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta cita ya pasó y no puede ser modificada")

    mascota = cita.mascota
    cliente = mascota.cliente

    for estado_actual, msg in [
        ("completado", "Esta cita ya fue completada y no puede ser modificada"),
        ("confirmado", "Esta cita ya fue confirmada previamente"),
        ("rechazado", "Esta cita ya fue rechazada previamente"),
    ]:
        if cita.estado == estado_actual:
            return CitaConfirmacionPublicResponse(
                id=cita.id, estado=cita.estado, fecha_hora=cita.fecha_hora,
                tipo_atencion=cita.tipo_atencion, nombre_mascota=mascota.nombre,
                nombre_cliente=cliente.nombre, message=msg
            )

    cita.estado = "confirmado"
    db.commit()
    return CitaConfirmacionPublicResponse(
        id=cita.id, estado=cita.estado, fecha_hora=cita.fecha_hora,
        tipo_atencion=cita.tipo_atencion, nombre_mascota=mascota.nombre,
        nombre_cliente=cliente.nombre, message="¡Cita confirmada exitosamente! Te esperamos."
    )


@router.get("/citas/rechazar", response_model=CitaConfirmacionPublicResponse, tags=["Citas Públicas"])
def rechazar_cita_publica(token: str, db: Session = Depends(get_db)):
    """Rechazar/cancelar una cita mediante token público."""
    cita = db.query(Cita).filter(Cita.confirmation_token == token).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enlace de cancelación inválido o expirado")

    if cita.fecha_hora < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta cita ya pasó y no puede ser modificada")

    mascota = cita.mascota
    cliente = mascota.cliente

    if cita.estado in ("rechazado", "completado"):
        return CitaConfirmacionPublicResponse(
            id=cita.id, estado=cita.estado, fecha_hora=cita.fecha_hora,
            tipo_atencion=cita.tipo_atencion, nombre_mascota=mascota.nombre,
            nombre_cliente=cliente.nombre, message="Esta cita ya fue procesada previamente"
        )
    if cita.estado == "confirmado":
        return CitaConfirmacionPublicResponse(
            id=cita.id, estado=cita.estado, fecha_hora=cita.fecha_hora,
            tipo_atencion=cita.tipo_atencion, nombre_mascota=mascota.nombre,
            nombre_cliente=cliente.nombre,
            message="Esta cita ya fue confirmada. Contacta a la veterinaria si deseas cancelarla."
        )

    cita.estado = "rechazado"
    db.commit()
    return CitaConfirmacionPublicResponse(
        id=cita.id, estado=cita.estado, fecha_hora=cita.fecha_hora,
        tipo_atencion=cita.tipo_atencion, nombre_mascota=mascota.nombre,
        nombre_cliente=cliente.nombre,
        message="Cita cancelada. Lamentamos no poder atenderte en esa fecha."
    )


@router.get("/citas/{cita_id}", response_model=CitaConDetallesResponse, tags=["Citas"])
def obtener_cita(
    cita_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cita.id == cita_id,
        Cliente.veterinaria_id == current.veterinaria_id
    )
    if current.rol == "veterinario":
        query = query.filter(Cita.veterinario_asignado_id == current.usuario_id)

    cita = query.first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")

    return _build_cita_response(cita)


@router.put("/citas/{cita_id}", response_model=CitaResponse, tags=["Citas"])
def actualizar_cita(
    cita_id: int,
    data: CitaUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Secretaria: puede actualizar cualquier campo.
    Veterinario: solo puede cancelar (estado=rechazado) sus propias citas.
    """
    query = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cita.id == cita_id,
        Cliente.veterinaria_id == current.veterinaria_id
    )
    if current.rol == "veterinario":
        query = query.filter(Cita.veterinario_asignado_id == current.usuario_id)

    cita = query.first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")

    estado_anterior = cita.estado

    # Veterinario solo puede cambiar estado
    if current.rol == "veterinario":
        if data.estado not in (None, "rechazado", "completado"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El veterinario solo puede cancelar o completar sus citas"
            )
        if data.estado:
            cita.estado = data.estado
    else:
        old_vet_id = cita.veterinario_asignado_id
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(cita, key, value)

        duracion = int(cita.duracion_minutos or 60)
        if duracion < 15 or duracion > 480:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La duración de la cita debe estar entre 15 y 480 minutos"
            )

        if _has_pet_datetime_conflict(
            db=db,
            veterinaria_id=current.veterinaria_id,
            mascota_id=cita.mascota_id,
            fecha_hora=cita.fecha_hora,
            duracion_minutos=duracion,
            exclude_cita_id=cita.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La mascota ya tiene una cita activa que se empalma con ese horario"
            )

        # Notificar al veterinario cuando se asigna o reasigna una cita
        new_vet_id = cita.veterinario_asignado_id
        if new_vet_id and new_vet_id != old_vet_id:
            asignacion = Notificacion(
                tipo="cita_asignada",
                mensaje=(
                    f"Se te asignó una cita: {cita.mascota.nombre} ({cita.mascota.cliente.nombre}) - "
                    f"{cita.fecha_hora.strftime('%d/%m/%Y %H:%M')} · {cita.tipo_atencion}"
                ),
                cita_id=cita.id,
                veterinaria_id=current.veterinaria_id,
                destinatario_usuario_id=new_vet_id
            )
            db.add(asignacion)

    db.commit()

    if estado_anterior != "rechazado" and cita.estado == "rechazado":
        _generar_sugerencias_lista_espera(
            db=db,
            veterinaria_id=current.veterinaria_id,
            cita_cancelada=cita
        )
        db.commit()

    db.refresh(cita)
    return cita


@router.delete("/citas/{cita_id}", response_model=MessageResponse, tags=["Citas"])
def eliminar_cita(
    cita_id: int,
    current: CurrentUser = Depends(require_role("secretaria")),
    db: Session = Depends(get_db)
):
    """Solo secretaria puede eliminar citas definitivamente."""
    cita = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cita.id == cita_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")

    db.query(Notificacion).filter(Notificacion.cita_id == cita_id).delete()
    db.delete(cita)
    db.commit()
    return MessageResponse(success=True, message="Cita eliminada exitosamente")


@router.put("/citas/{cita_id}/recordatorio-whatsapp", response_model=CitaResponse, tags=["Citas"])
def marcar_recordatorio_whatsapp(
    cita_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cita = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cita.id == cita_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")

    cita.recordatorio_whatsapp_enviado = 1
    db.commit()
    db.refresh(cita)
    return cita


@router.put("/citas/{cita_id}/recordatorio-email", response_model=CitaResponse, tags=["Citas"])
def marcar_recordatorio_email(
    cita_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cita = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cita.id == cita_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")

    cita.recordatorio_email_enviado = 1
    db.commit()
    db.refresh(cita)
    return cita
