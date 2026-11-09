import type {
  ListaEsperaItem,
  ListaEsperaCreate,
} from '../../domain/models/listaEspera';
import type { Cita } from '../../domain/models/cita';
import {
  crearItemListaEspera,
  actualizarItemListaEspera,
  convertirListaEsperaEnCita,
} from '../../infrastructure/api/listaEsperaService';

export interface GuardarListaEsperaInput {
  itemId?: number | null;
  mascotaId: number;
  tipoAtencion: string;
  duracionMinutos?: number;
  prioridad?: number;
  horaInicioRaw?: string;
  horaFinRaw?: string;
  notas?: string;
  preferenciaVeterinarioId?: number;
}

export function estadoWaitlistLabel(estado: string): string {
  if (estado === 'activa') return 'Activa';
  if (estado === 'contactado') return 'Contactado';
  if (estado === 'convertida') return 'Convertida';
  if (estado === 'descartada') return 'Descartada';
  return estado;
}

export async function guardarListaEsperaUseCase(
  input: GuardarListaEsperaInput
): Promise<ListaEsperaItem> {
  if (Number.isNaN(input.mascotaId) || input.mascotaId <= 0) {
    throw new Error('Selecciona una mascota');
  }

  if (!input.tipoAtencion || !input.tipoAtencion.trim()) {
    throw new Error('Especifica el tipo de atencion');
  }

  const horaInicioRaw = (input.horaInicioRaw || '').trim();
  const horaFinRaw = (input.horaFinRaw || '').trim();
  const horaInicio = horaInicioRaw === '' ? undefined : parseInt(horaInicioRaw, 10);
  const horaFin = horaFinRaw === '' ? undefined : parseInt(horaFinRaw, 10);

  if ((horaInicio != null && Number.isNaN(horaInicio)) || (horaFin != null && Number.isNaN(horaFin))) {
    throw new Error('Las horas preferidas no son validas');
  }

  if (horaInicio != null && horaFin != null && horaInicio > horaFin) {
    throw new Error('La hora de inicio no puede ser mayor que la hora de fin');
  }

  const payload: ListaEsperaCreate = {
    mascota_id: input.mascotaId,
    tipo_atencion: input.tipoAtencion.trim(),
    duracion_minutos: input.duracionMinutos ?? 60,
    prioridad: input.prioridad ?? 0,
    hora_inicio_preferida: horaInicio,
    hora_fin_preferida: horaFin,
    notas: input.notas?.trim() || undefined,
    preferencia_veterinario_id: input.preferenciaVeterinarioId,
  };

  if (input.itemId && !Number.isNaN(input.itemId) && input.itemId > 0) {
    return await actualizarItemListaEspera(input.itemId, payload);
  }

  return await crearItemListaEspera(payload);
}

export async function convertirListaEsperaUseCase(params: {
  itemId: number;
  citaReferenciaId?: number;
  fechaHora?: string;
  veterinarioAsignadoId?: number;
}): Promise<Cita> {
  if (!params.itemId || params.itemId <= 0) {
    throw new Error('ID de elemento de lista de espera inválido');
  }
  return await convertirListaEsperaEnCita(params);
}
