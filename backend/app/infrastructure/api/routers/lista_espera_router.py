from datetime import datetime
from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.dtos.cita_dto import CitaResponse
from app.application.dtos.common_dto import MessageResponse
from app.application.dtos.lista_espera_dto import (
    ListaEsperaCreate, ListaEsperaUpdate, ListaEsperaResponse,
)
from app.infrastructure.persistence.models import (
    Veterinaria, Usuario, Cliente, Mascota, Bitacora, Cita, ListaEspera, Notificacion
)
from app.infrastructure.api.dependencies import CurrentUser, get_current_user, require_role, get_db
from app.infrastructure.api.cita_helpers import _build_lista_espera_response, _has_pet_datetime_conflict

router = APIRouter()

@router.post("/lista-espera", response_model=ListaEsperaResponse, tags=["Lista de Espera"])
def crear_item_lista_espera(
    data: ListaEsperaCreate,
    current: CurrentUser = Depends(require_role("secretaria")),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).join(Cliente).filter(
        Mascota.id == data.mascota_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")

    duracion = int(data.duracion_minutos or 60)
    if duracion < 15 or duracion > 480:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración debe estar entre 15 y 480 minutos"
        )

    if data.hora_inicio_preferida is not None and (data.hora_inicio_preferida < 0 or data.hora_inicio_preferida > 23):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora de inicio preferida debe estar entre 0 y 23")
    if data.hora_fin_preferida is not None and (data.hora_fin_preferida < 0 or data.hora_fin_preferida > 23):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora de fin preferida debe estar entre 0 y 23")
    if data.hora_inicio_preferida is not None and data.hora_fin_preferida is not None and data.hora_inicio_preferida > data.hora_fin_preferida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora de inicio preferida no puede ser mayor que la hora de fin")

    preferencia_vet = None
    if data.preferencia_veterinario_id:
        preferencia_vet = db.query(Usuario).filter(
            Usuario.id == data.preferencia_veterinario_id,
            Usuario.veterinaria_id == current.veterinaria_id,
            Usuario.rol == "veterinario",
            Usuario.activo == 1
        ).first()
        if not preferencia_vet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El veterinario de preferencia no es válido"
            )

    item = ListaEspera(
        tipo_atencion=data.tipo_atencion,
        duracion_minutos=duracion,
        prioridad=int(data.prioridad or 0),
        hora_inicio_preferida=data.hora_inicio_preferida,
        hora_fin_preferida=data.hora_fin_preferida,
        notas=data.notas,
        mascota_id=data.mascota_id,
        veterinaria_id=current.veterinaria_id,
        preferencia_veterinario_id=preferencia_vet.id if preferencia_vet else None,
        estado="activa"
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _build_lista_espera_response(item)


@router.get("/lista-espera", response_model=List[ListaEsperaResponse], tags=["Lista de Espera"])
def listar_lista_espera(
    estado: Optional[str] = None,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ListaEspera).join(Mascota).join(Cliente).filter(
        ListaEspera.veterinaria_id == current.veterinaria_id,
        Cliente.veterinaria_id == current.veterinaria_id
    )
    if estado:
        query = query.filter(ListaEspera.estado == estado)

    items = query.order_by(ListaEspera.prioridad.desc(), ListaEspera.fecha_creacion.asc()).all()
    return [_build_lista_espera_response(item) for item in items]


@router.get("/lista-espera/{item_id}", response_model=ListaEsperaResponse, tags=["Lista de Espera"])
def obtener_item_lista_espera(
    item_id: int,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(ListaEspera).join(Mascota).join(Cliente).filter(
        ListaEspera.id == item_id,
        ListaEspera.veterinaria_id == current.veterinaria_id,
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elemento no encontrado")
    return _build_lista_espera_response(item)


@router.put("/lista-espera/{item_id}", response_model=ListaEsperaResponse, tags=["Lista de Espera"])
def actualizar_item_lista_espera(
    item_id: int,
    data: ListaEsperaUpdate,
    current: CurrentUser = Depends(require_role("secretaria")),
    db: Session = Depends(get_db)
):
    item = db.query(ListaEspera).filter(
        ListaEspera.id == item_id,
        ListaEspera.veterinaria_id == current.veterinaria_id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elemento no encontrado")

    updates = data.model_dump(exclude_unset=True)

    if "duracion_minutos" in updates:
        duracion = int(updates["duracion_minutos"] or 60)
        if duracion < 15 or duracion > 480:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La duración debe estar entre 15 y 480 minutos"
            )
        item.duracion_minutos = duracion
        updates.pop("duracion_minutos")

    if "preferencia_veterinario_id" in updates and updates["preferencia_veterinario_id"]:
        preferencia_vet = db.query(Usuario).filter(
            Usuario.id == updates["preferencia_veterinario_id"],
            Usuario.veterinaria_id == current.veterinaria_id,
            Usuario.rol == "veterinario",
            Usuario.activo == 1
        ).first()
        if not preferencia_vet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El veterinario de preferencia no es válido"
            )

    for field_name in ("hora_inicio_preferida", "hora_fin_preferida"):
        if field_name in updates and updates[field_name] is not None:
            hour_val = int(updates[field_name])
            if hour_val < 0 or hour_val > 23:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Las horas preferidas deben estar entre 0 y 23"
                )
            updates[field_name] = hour_val

    hora_inicio_final = updates.get("hora_inicio_preferida", item.hora_inicio_preferida)
    hora_fin_final = updates.get("hora_fin_preferida", item.hora_fin_preferida)
    if hora_inicio_final is not None and hora_fin_final is not None and hora_inicio_final > hora_fin_final:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La hora de inicio preferida no puede ser mayor que la hora de fin"
        )

    for key, value in updates.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return _build_lista_espera_response(item)


@router.delete("/lista-espera/{item_id}", response_model=MessageResponse, tags=["Lista de Espera"])
def eliminar_item_lista_espera(
    item_id: int,
    current: CurrentUser = Depends(require_role("secretaria")),
    db: Session = Depends(get_db)
):
    item = db.query(ListaEspera).filter(
        ListaEspera.id == item_id,
        ListaEspera.veterinaria_id == current.veterinaria_id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elemento no encontrado")

    db.delete(item)
    db.commit()
    return MessageResponse(success=True, message="Elemento de lista de espera eliminado")


@router.post("/lista-espera/{item_id}/convertir", response_model=CitaResponse, tags=["Lista de Espera"])
def convertir_item_lista_espera_a_cita(
    item_id: int,
    cita_referencia_id: Optional[int] = None,
    fecha_hora: Optional[datetime] = None,
    veterinario_asignado_id: Optional[int] = None,
    current: CurrentUser = Depends(require_role("secretaria")),
    db: Session = Depends(get_db)
):
    item = db.query(ListaEspera).join(Mascota).join(Cliente).filter(
        ListaEspera.id == item_id,
        ListaEspera.veterinaria_id == current.veterinaria_id,
        ListaEspera.estado == "activa",
        Cliente.veterinaria_id == current.veterinaria_id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elemento de lista de espera no encontrado o no activo")

    cita_ref = None
    if cita_referencia_id:
        cita_ref = db.query(Cita).join(Mascota).join(Cliente).filter(
            Cita.id == cita_referencia_id,
            Cliente.veterinaria_id == current.veterinaria_id
        ).first()
        if not cita_ref:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita de referencia no encontrada")

    fecha_objetivo = fecha_hora or (cita_ref.fecha_hora if cita_ref else None)
    if not fecha_objetivo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes proporcionar fecha_hora o cita_referencia_id"
        )

    vet_id = veterinario_asignado_id or (cita_ref.veterinario_asignado_id if cita_ref else item.preferencia_veterinario_id)
    if not vet_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes seleccionar un veterinario para convertir la sugerencia"
        )

    vet = db.query(Usuario).filter(
        Usuario.id == vet_id,
        Usuario.veterinaria_id == current.veterinaria_id,
        Usuario.rol == "veterinario",
        Usuario.activo == 1
    ).first()
    if not vet:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Veterinario no válido")

    duracion = int(item.duracion_minutos or 60)
    if _has_pet_datetime_conflict(
        db=db,
        veterinaria_id=current.veterinaria_id,
        mascota_id=item.mascota_id,
        fecha_hora=fecha_objetivo,
        duracion_minutos=duracion
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La mascota ya tiene una cita activa que se empalma con ese horario"
        )

    nueva_cita = Cita(
        fecha_hora=fecha_objetivo,
        tipo_atencion=item.tipo_atencion,
        descripcion=item.notas,
        duracion_minutos=duracion,
        estado="pendiente",
        mascota_id=item.mascota_id,
        veterinario_asignado_id=vet.id,
        confirmation_token=str(uuid.uuid4())
    )
    db.add(nueva_cita)
    db.flush()

    item.estado = "convertida"

    db.add(Notificacion(
        tipo="cita_asignada",
        mensaje=(
            f"Se te asignó una cita desde lista de espera: {item.mascota.nombre} "
            f"({item.mascota.cliente.nombre}) - {fecha_objetivo.strftime('%d/%m/%Y %H:%M')} · {item.tipo_atencion}"
        ),
        cita_id=nueva_cita.id,
        veterinaria_id=current.veterinaria_id,
        destinatario_usuario_id=vet.id
    ))

    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita
