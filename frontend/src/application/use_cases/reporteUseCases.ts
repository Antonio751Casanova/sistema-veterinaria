import type { CitaConDetalles } from '../../domain/models/cita';
import type { Bitacora, BitacoraCreate } from '../../domain/models/bitacora';
import {
  listarBitacora,
  crearEntradaBitacora,
  eliminarEntradaBitacora,
} from '../../infrastructure/api/bitacoraService';

export const TIPOS_ATENCION: string[] = [
  'Consulta General','Consulta de Emergencia','Consulta de Seguimiento','Primera Consulta','Segunda Opinion',
  'Vacunacion','Vacunacion Cachorro','Vacunacion Adulto','Vacunacion Antirabica','Refuerzo de Vacunas',
  'Desparasitacion Interna','Desparasitacion Externa','Control de Pulgas y Garrapatas',
  'Cirugia General','Cirugia de Emergencia','Esterilizacion','Castracion','Cirugia Ortopedica','Extraccion Dental','Cirugia de Tumor',
  'Limpieza Dental','Revision Dental','Extraccion de Diente',
  'Radiografia','Ecografia','Electrocardiograma','Analisis de Sangre','Analisis de Orina','Analisis de Heces','Citologia','Biopsia',
  'Grooming','Bano y Corte','Corte de Unas','Limpieza de Oidos','Limpieza de Glandulas Anales',
  'Control de Peso','Revision Geriatrica','Chequeo Preventivo','Control Prenatal','Control Postparto',
  'Revision Post-operatoria','Retiro de Puntos','Curacion de Heridas',
  'Hospitalizacion','Quimioterapia','Fisioterapia','Aplicacion de Medicamentos','Nebulizacion',
  'Microchip','Certificado de Salud','Eutanasia','Cremacion',
];

export const ESTADO_LABELS: Record<string, string> = {
  confirmado: 'Confirmado',
  rechazado: 'Rechazado',
  pendiente: 'Pendiente',
};

export const ESTADO_BADGES: Record<string, string> = {
  confirmado: 'rpt-badge-confirmado',
  rechazado: 'rpt-badge-rechazado',
  pendiente: 'rpt-badge-pendiente',
};

export const SPECIES_EMOJI: Record<string, string> = {
  Perro: '🐕',
  Gato: '🐱',
  Ave: '🦜',
  Roedor: '🐹',
  Reptil: '🦎',
  Otro: '🐾',
};

export const SPLIT_THRESHOLD = 500;

export interface ReportFilterCriteria {
  desde: string;
  hasta: string;
  estado?: string;
  tipo?: string;
}

export interface ReportStats {
  total: number;
  confirmado: number;
  rechazado: number;
}

export function fmtDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

export function fmtTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

export function fmtDateLong(dateStr: string): string {
  const [y, m, d] = dateStr.split('-');
  return new Date(+y, +m - 1, +d).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' });
}

export function computeStats(citas: CitaConDetalles[]): ReportStats {
  return {
    total: citas.length,
    confirmado: citas.filter(c => c.estado === 'confirmado').length,
    rechazado: citas.filter(c => c.estado === 'rechazado').length,
  };
}

export function groupByMonth(citas: CitaConDetalles[]): Map<string, CitaConDetalles[]> {
  const groups = new Map<string, CitaConDetalles[]>();
  for (const c of citas) {
    const key = c.fecha_hora.substring(0, 7); // "YYYY-MM"
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(c);
  }
  return new Map([...groups.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

export function monthLabel(yearMonth: string): string {
  const [y, m] = yearMonth.split('-');
  const date = new Date(+y, +m - 1, 1);
  const label = date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export function validateReportFilterDates(desde: string, hasta: string): string | null {
  if (!desde || !hasta) {
    return 'Por favor selecciona el rango de fechas (Desde y Hasta).';
  }
  if (desde > hasta) {
    return 'La fecha "Desde" no puede ser posterior a la fecha "Hasta".';
  }
  return null;
}

export function filterReportCitasUseCase(
  todasCitas: CitaConDetalles[],
  criteria: ReportFilterCriteria
): CitaConDetalles[] {
  const validationError = validateReportFilterDates(criteria.desde, criteria.hasta);
  if (validationError) {
    throw new Error(validationError);
  }

  const estado = criteria.estado || '';
  const tipo = (criteria.tipo || '').toLowerCase().trim();

  const filtered = todasCitas.filter(c => {
    const fechaStr = c.fecha_hora.split('T')[0];
    if (fechaStr < criteria.desde || fechaStr > criteria.hasta) return false;
    if (estado && c.estado !== estado) return false;
    if (tipo && !c.tipo_atencion.toLowerCase().includes(tipo)) return false;
    return true;
  });

  filtered.sort((a, b) => new Date(a.fecha_hora).getTime() - new Date(b.fecha_hora).getTime());
  return filtered;
}

// ==========================================
// Bitácora de Mascotas Use Cases
// ==========================================

export function formatBitacoraDateTime(iso: string): { fecha: string; hora: string } {
  const dateObj = new Date(iso);
  const fecha = dateObj.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
  const hora = dateObj.toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
  });
  return { fecha, hora };
}

export async function listarBitacoraUseCase(mascotaId: number): Promise<Bitacora[]> {
  if (!mascotaId || mascotaId <= 0) {
    throw new Error('ID de mascota inválido');
  }
  return await listarBitacora(mascotaId);
}

export async function crearEntradaBitacoraUseCase(
  mascotaId: number,
  data: BitacoraCreate
): Promise<Bitacora> {
  if (!mascotaId || mascotaId <= 0) {
    throw new Error('ID de mascota inválido');
  }
  if (!data.tipo?.trim() || !data.descripcion?.trim()) {
    throw new Error('El tipo y la descripción son obligatorios');
  }
  return await crearEntradaBitacora(mascotaId, {
    tipo: data.tipo.trim(),
    descripcion: data.descripcion.trim(),
    tratamiento: data.tratamiento?.trim() || undefined,
    medicamentos: data.medicamentos?.trim() || undefined,
    costo: data.costo?.trim() || undefined,
    proxima_cita: data.proxima_cita?.trim() || undefined,
  });
}

export async function eliminarEntradaBitacoraUseCase(
  mascotaId: number,
  entradaId: number
): Promise<void> {
  if (!mascotaId || !entradaId) {
    throw new Error('Parámetros inválidos para eliminar registro de bitácora');
  }
  await eliminarEntradaBitacora(mascotaId, entradaId);
}
