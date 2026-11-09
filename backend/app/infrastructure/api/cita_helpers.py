"""Helpers compartidos por los routers de Citas y Lista de Espera (Avance 2)."""
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.application.dtos.cita_dto import CitaConDetallesResponse
from app.application.dtos.lista_espera_dto import ListaEsperaResponse
from app.infrastructure.persistence.models import (
    Veterinaria, Usuario, Cliente, Mascota, Bitacora, Cita, ListaEspera, Notificacion
)

def _build_cita_response(cita: Cita) -> CitaConDetallesResponse:
    mascota = cita.mascota
    cliente = mascota.cliente
    vet_nombre = cita.veterinario_asignado.nombre if cita.veterinario_asignado else None
    return CitaConDetallesResponse(
        id=cita.id,
        fecha_hora=cita.fecha_hora,
        duracion_minutos=cita.duracion_minutos,
        tipo_atencion=cita.tipo_atencion,
        descripcion=cita.descripcion,
        tratamiento=cita.tratamiento,
        medicamento=cita.medicamento,
        costo=cita.costo,
        estado=cita.estado,
        mascota_id=cita.mascota_id,
        recordatorio_whatsapp_enviado=cita.recordatorio_whatsapp_enviado,
        recordatorio_email_enviado=cita.recordatorio_email_enviado,
        fecha_creacion=cita.fecha_creacion,
        nombre_mascota=mascota.nombre,
        especie_mascota=mascota.especie,
        nombre_cliente=cliente.nombre,
        telefono_cliente=cliente.telefono,
        email_cliente=cliente.email,
        confirmation_token=cita.confirmation_token,
        veterinario_asignado_id=cita.veterinario_asignado_id,
        nombre_veterinario_asignado=vet_nombre
    )


def _build_lista_espera_response(item: ListaEspera) -> ListaEsperaResponse:
    mascota = item.mascota
    cliente = mascota.cliente
    vet_nombre = item.preferencia_veterinario.nombre if item.preferencia_veterinario else None
    return ListaEsperaResponse(
        id=item.id,
        tipo_atencion=item.tipo_atencion,
        duracion_minutos=item.duracion_minutos,
        prioridad=item.prioridad,
        hora_inicio_preferida=item.hora_inicio_preferida,
        hora_fin_preferida=item.hora_fin_preferida,
        notas=item.notas,
        preferencia_veterinario_id=item.preferencia_veterinario_id,
        mascota_id=item.mascota_id,
        veterinaria_id=item.veterinaria_id,
        estado=item.estado,
        fecha_creacion=item.fecha_creacion,
        nombre_mascota=mascota.nombre,
        especie_mascota=mascota.especie,
        nombre_cliente=cliente.nombre,
        telefono_cliente=cliente.telefono,
        preferencia_veterinario_nombre=vet_nombre
    )


def _score_waitlist_candidate(db: Session, item: ListaEspera, cita: Cita) -> int:
    """Puntaje simple para sugerencias automáticas cuando se libera un hueco."""
    score = 0

    if item.tipo_atencion.strip().lower() == cita.tipo_atencion.strip().lower():
        score += 40

    duracion_item = item.duracion_minutos or 60
    duracion_cita = cita.duracion_minutos or 60
    if duracion_item <= duracion_cita:
        score += 25
    else:
        score -= min(20, duracion_item - duracion_cita)

    if item.preferencia_veterinario_id and item.preferencia_veterinario_id == cita.veterinario_asignado_id:
        score += 20

    if item.hora_inicio_preferida is not None and item.hora_fin_preferida is not None:
        cita_hour = cita.fecha_hora.hour
        if item.hora_inicio_preferida <= cita_hour <= item.hora_fin_preferida:
            score += 15
        else:
            score -= 8

    score += max(-20, min(20, int(item.prioridad or 0) * 4))

    edad_horas = (datetime.utcnow() - item.fecha_creacion).total_seconds() / 3600
    score += min(20, int(edad_horas // 24))

    no_show_count = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == item.veterinaria_id,
        Cita.mascota_id == item.mascota_id,
        Cita.estado == "rechazado",
        Cita.fecha_hora <= datetime.utcnow(),
        Cita.fecha_hora >= (datetime.utcnow() - timedelta(days=90))
    ).count()
    score -= min(15, no_show_count * 5)

    return score


def _generar_sugerencias_lista_espera(
    db: Session,
    veterinaria_id: int,
    cita_cancelada: Cita,
    max_sugerencias: int = 3
):
    candidatos = db.query(ListaEspera).join(Mascota).join(Cliente).filter(
        ListaEspera.veterinaria_id == veterinaria_id,
        ListaEspera.estado == "activa",
        Cliente.veterinaria_id == veterinaria_id
    ).all()

    if not candidatos:
        return

    ranking = sorted(
        ((item, _score_waitlist_candidate(db, item, cita_cancelada)) for item in candidatos),
        key=lambda tup: tup[1],
        reverse=True
    )
    top = ranking[:max_sugerencias]
    if not top:
        return

    resumen = " | ".join([
        f"LE#{item.id} {item.mascota.nombre} ({item.mascota.cliente.nombre}) p={score}"
        for item, score in top
    ])
    mensaje = (
        f"Se liberó un hueco por cancelación el {cita_cancelada.fecha_hora.strftime('%d/%m/%Y %H:%M')} "
        f"({cita_cancelada.tipo_atencion}). Sugerencias lista de espera: {resumen}"
    )
    notificacion = Notificacion(
        tipo="lista_espera_sugerencia",
        mensaje=mensaje,
        cita_id=cita_cancelada.id,
        veterinaria_id=veterinaria_id
    )
    db.add(notificacion)


def _has_pet_datetime_conflict(
    db: Session,
    veterinaria_id: int,
    mascota_id: int,
    fecha_hora: datetime,
    duracion_minutos: int,
    exclude_cita_id: Optional[int] = None
) -> bool:
    start = fecha_hora
    end = fecha_hora + timedelta(minutes=duracion_minutos)

    query = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == veterinaria_id,
        Cita.mascota_id == mascota_id,
        Cita.estado.notin_(["rechazado", "completado"])
    )
    if exclude_cita_id:
        query = query.filter(Cita.id != exclude_cita_id)
    for c in query.all():
        c_start = c.fecha_hora
        c_end = c_start + timedelta(minutes=(c.duracion_minutos or 60))
        if start < c_end and end > c_start:
            return True
    return False
