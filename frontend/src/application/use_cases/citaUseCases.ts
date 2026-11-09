import type { CitaConDetalles, CitaCreate, CitaUpdate } from '../../domain/models/cita';
import { actualizarCita, crearCita } from '../../infrastructure/api/citaService';

const DURACIONES_KEY = 'vet_cita_duraciones';

export const estadoBadges: Record<string, string> = {
  pendiente: 'bg-yellow-500/20 text-yellow-700',
  confirmado: 'bg-blue-500/20 text-blue-700',
  en_espera: 'bg-sky-500/20 text-sky-700',
  completado: 'bg-gray-500/20 text-gray-600',
  rechazado: 'bg-red-500/20 text-red-700',
};

export const estadoLabels: Record<string, string> = {
  pendiente: 'Pendiente',
  confirmado: 'Confirmado',
  en_espera: 'En Espera',
  completado: 'Completado',
  rechazado: 'Rechazado',
};

export function loadDuracionesMap(): Record<string, number> {
  try {
    return JSON.parse(localStorage.getItem(DURACIONES_KEY) || '{}');
  } catch {
    return {};
  }
}

export function saveCitaDuracion(citaId: number, duracion: number): void {
  const map = loadDuracionesMap();
  map[citaId] = duracion;
  localStorage.setItem(DURACIONES_KEY, JSON.stringify(map));
}

export function getCitaDuracion(citaId: number): number {
  return loadDuracionesMap()[citaId] ?? 60;
}

export function filterCitasUseCase(
  citas: CitaConDetalles[],
  params: {
    searchTerm: string;
    estadoValue: string;
    fechaValue: string;
    vetFilterValue: string;
    userRol: string;
  }
): CitaConDetalles[] {
  const term = params.searchTerm.toLowerCase().trim();
  const searchDigits = term.replace(/\D/g, '');

  const filtered = citas.filter((cita) => {
    let matchesSearch = true;
    if (term) {
      const phoneMatch =
        searchDigits.length >= 3 &&
        (cita.telefono_cliente || '').replace(/\D/g, '').includes(searchDigits);
      matchesSearch =
        cita.nombre_mascota?.toLowerCase().includes(term) ||
        cita.nombre_cliente?.toLowerCase().includes(term) ||
        phoneMatch ||
        cita.tipo_atencion.toLowerCase().includes(term) ||
        false;
    }

    let matchesEstado = true;
    if (params.estadoValue) {
      matchesEstado = cita.estado === params.estadoValue;
    }

    let matchesFecha = true;
    if (params.fechaValue) {
      const citaFechaStr = cita.fecha_hora.split('T')[0];
      matchesFecha = citaFechaStr === params.fechaValue;
    }

    let matchesVet = true;
    if (params.vetFilterValue && params.userRol === 'secretaria') {
      matchesVet = cita.veterinario_asignado_id?.toString() === params.vetFilterValue;
    }

    return matchesSearch && matchesEstado && matchesFecha && matchesVet;
  });

  filtered.sort((a, b) => new Date(b.fecha_hora).getTime() - new Date(a.fecha_hora).getTime());
  return filtered;
}

export async function guardarCitaUseCase(params: {
  id: number | null;
  selectedClienteId: number | null;
  mascotaId: number;
  fecha: string;
  hora: string;
  duracionMinutos: number;
  tipoAtencion: string;
  estado: string;
  detalles: string;
  veterinarioAsignadoId?: number;
  userRol: string;
  hasConflict: boolean;
}): Promise<void> {
  if (!params.selectedClienteId) {
    throw new Error('Por favor selecciona un cliente');
  }
  if (!params.mascotaId) {
    throw new Error('Por favor selecciona una mascota');
  }
  if (!params.fecha || !params.hora) {
    throw new Error('Por favor completa la fecha y hora');
  }
  if (!params.tipoAtencion.trim()) {
    throw new Error('Por favor selecciona o escribe el tipo de atencion');
  }
  if (params.userRol === 'secretaria' && !params.veterinarioAsignadoId) {
    throw new Error('Por favor selecciona un veterinario para la cita');
  }
  if (params.hasConflict) {
    throw new Error('La hora seleccionada se empalma con otra cita. Por favor elige una hora diferente.');
  }

  const citaData: CitaCreate = {
    mascota_id: params.mascotaId,
    fecha_hora: `${params.fecha}T${params.hora}:00`,
    duracion_minutos: params.duracionMinutos,
    tipo_atencion: params.tipoAtencion,
    estado: params.estado,
    costo: undefined,
    descripcion: params.detalles || undefined,
    veterinario_asignado_id: params.veterinarioAsignadoId,
  };

  if (params.id) {
    await actualizarCita(params.id, citaData as CitaUpdate);
    saveCitaDuracion(params.id, citaData.duracion_minutos || 60);
  } else {
    const newCita = await crearCita(citaData);
    saveCitaDuracion(newCita.id, citaData.duracion_minutos || 60);
  }
}

