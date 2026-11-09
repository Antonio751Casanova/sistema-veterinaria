from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.persistence.models import Cliente, Mascota, Cita
from app.infrastructure.api.dependencies import CurrentUser, get_current_user, require_role, get_db

router = APIRouter()

@router.get("/estadisticas", tags=["Estadísticas"])
def obtener_estadisticas(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    veterinario_id: Optional[int] = None
):
    """
    Secretaria: puede filtrar por veterinario_id (opcional).
    Veterinario: solo ve estadísticas de sus propias citas.
    """
    from sqlalchemy import func
    from datetime import date

    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    vet_filter_id = None
    if current.rol == "veterinario":
        vet_filter_id = current.usuario_id
    elif veterinario_id:
        vet_filter_id = veterinario_id

    total_clientes = db.query(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id
    ).count()
    clientes_hoy = db.query(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id,
        func.date(Cliente.fecha_creacion) == today
    ).count()
    clientes_semana = db.query(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id,
        func.date(Cliente.fecha_creacion) >= week_ago
    ).count()
    clientes_mes = db.query(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id,
        func.date(Cliente.fecha_creacion) >= month_ago
    ).count()

    total_mascotas = db.query(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id
    ).count()
    especies = db.query(
        Mascota.especie, func.count(Mascota.id).label('cantidad')
    ).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id
    ).group_by(Mascota.especie).all()

    cita_query = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id
    )
    if vet_filter_id:
        cita_query = cita_query.filter(Cita.veterinario_asignado_id == vet_filter_id)

    total_citas = cita_query.count()
    citas_pendientes = cita_query.filter(Cita.estado == "pendiente").count()
    citas_hoy = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id,
        func.date(Cita.fecha_hora) == today,
        *([Cita.veterinario_asignado_id == vet_filter_id] if vet_filter_id else [])
    ).count()
    citas_semana = db.query(Cita).join(Mascota).join(Cliente).filter(
        Cliente.veterinaria_id == current.veterinaria_id,
        func.date(Cita.fecha_hora) >= today,
        func.date(Cita.fecha_hora) <= today + timedelta(days=7),
        *([Cita.veterinario_asignado_id == vet_filter_id] if vet_filter_id else [])
    ).count()

    return {
        "clientes": {
            "total": total_clientes, "hoy": clientes_hoy,
            "semana": clientes_semana, "mes": clientes_mes
        },
        "mascotas": {
            "total": total_mascotas,
            "por_especie": [{"especie": e[0], "cantidad": e[1]} for e in especies]
        },
        "citas": {
            "total": total_citas, "pendientes": citas_pendientes,
            "hoy": citas_hoy, "semana": citas_semana
        }
    }
