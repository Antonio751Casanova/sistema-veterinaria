import { API_BASE_URL } from '../config/api';

export interface EspecieData {
  especie: string;
  cantidad: number;
}

export interface Estadisticas {
  clientes: {
    total: number;
    hoy: number;
    semana: number;
    mes: number;
  };
  mascotas: {
    total: number;
    por_especie: EspecieData[];
  };
  citas: {
    total: number;
    pendientes: number;
    hoy: number;
    semana: number;
  };
}

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

export async function obtenerEstadisticas(): Promise<Estadisticas> {
  const response = await fetch(`${API_BASE_URL}/estadisticas`, {
    method: 'GET',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al obtener estadísticas');
  }

  return response.json();
}
