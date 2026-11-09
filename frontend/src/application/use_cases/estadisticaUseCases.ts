import type { Cliente } from '../../domain/models/cliente';
import type { Mascota } from '../../domain/models/mascota';
import type { CitaConDetalles } from '../../domain/models/cita';
import type { Estadisticas } from '../../domain/models/estadistica';
import { obtenerEstadisticas } from '../../infrastructure/api/estadisticaService';

export const SPECIES_EMOJIS: Record<string, string> = {
  'Perro': '🐕',
  'Gato': '🐱',
  'Ave': '🦜',
  'Roedor': '🐹',
  'Reptil': '🦎',
  'Otro': '🐾',
};

export interface EstadisticasSummary {
  totalClientes: number;
  totalMascotas: number;
  totalCitas: number;
  promedioMascotas: string;
}

export async function obtenerEstadisticasUseCase(): Promise<Estadisticas> {
  return await obtenerEstadisticas();
}

export function computeEstadisticasSummary(
  clientes: Cliente[],
  mascotas: Mascota[],
  citas: CitaConDetalles[]
): EstadisticasSummary {
  const totalClientes = clientes.length;
  const totalMascotas = mascotas.length;
  const totalCitas = citas.length;
  const promedioMascotas = totalClientes > 0
    ? (totalMascotas / totalClientes).toFixed(1)
    : '0';

  return {
    totalClientes,
    totalMascotas,
    totalCitas,
    promedioMascotas,
  };
}

export function computeSpeciesDistribution(mascotas: Mascota[]): {
  labels: string[];
  data: number[];
  colors: string[];
} {
  const speciesCount: Record<string, number> = {};
  mascotas.forEach(m => {
    speciesCount[m.especie] = (speciesCount[m.especie] || 0) + 1;
  });

  const rawLabels = Object.keys(speciesCount);
  const data = Object.values(speciesCount);
  const palette = [
    'rgba(245, 158, 11, 0.8)',  // amber
    'rgba(168, 85, 247, 0.8)',  // purple
    'rgba(14, 165, 233, 0.8)',  // sky
    'rgba(236, 72, 153, 0.8)',  // pink
    'rgba(132, 204, 22, 0.8)',  // lime
    'rgba(107, 114, 128, 0.8)', // gray
  ];

  return {
    labels: rawLabels.map(l => `${SPECIES_EMOJIS[l] || '🐾'} ${l}`),
    data,
    colors: palette.slice(0, rawLabels.length),
  };
}

export function computeCitasByEstado(citas: CitaConDetalles[]): {
  labels: string[];
  data: number[];
  colors: string[];
} {
  const estadoCount: Record<string, number> = {
    pendiente: 0,
    confirmado: 0,
    en_espera: 0,
    completado: 0,
    rechazado: 0,
  };

  citas.forEach(c => {
    if (estadoCount[c.estado] !== undefined) {
      estadoCount[c.estado]++;
    }
  });

  return {
    labels: ['Pendiente', 'Confirmado', 'En Espera', 'Completado', 'Rechazado'],
    data: [
      estadoCount['pendiente'],
      estadoCount['confirmado'],
      estadoCount['en_espera'],
      estadoCount['completado'],
      estadoCount['rechazado'],
    ],
    colors: [
      'rgba(234, 179, 8, 0.8)',   // yellow
      'rgba(16, 185, 129, 0.8)',  // emerald
      'rgba(14, 165, 233, 0.8)',  // sky
      'rgba(107, 114, 128, 0.8)', // gray
      'rgba(239, 68, 68, 0.8)',   // red
    ],
  };
}

export function computeMonthlyClientRegistrations(clientes: Cliente[]): {
  labels: string[];
  data: number[];
} {
  const monthlyCount: Record<string, number> = {};
  const now = new Date();

  for (let i = 5; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    monthlyCount[key] = 0;
  }

  clientes.forEach(c => {
    const d = new Date(c.fecha_creacion);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
    if (monthlyCount[key] !== undefined) {
      monthlyCount[key]++;
    }
  });

  const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const labels = Object.keys(monthlyCount).map(k => {
    const [year, month] = k.split('-');
    return `${monthNames[parseInt(month, 10) - 1]} ${year}`;
  });
  const data = Object.values(monthlyCount);

  return { labels, data };
}

export function formatShortDate(date: string): string {
  return new Date(date).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
}

export function getRecentClientes(clientes: Cliente[], limit = 5): Cliente[] {
  return [...clientes]
    .sort((a, b) => new Date(b.fecha_creacion).getTime() - new Date(a.fecha_creacion).getTime())
    .slice(0, limit);
}

export function getRecentMascotas(mascotas: Mascota[], limit = 5): Mascota[] {
  return [...mascotas]
    .sort((a, b) => new Date(b.fecha_creacion).getTime() - new Date(a.fecha_creacion).getTime())
    .slice(0, limit);
}
