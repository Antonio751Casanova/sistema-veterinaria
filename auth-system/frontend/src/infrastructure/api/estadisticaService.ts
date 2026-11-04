import { API_BASE_URL, buildAuthHeaders } from './api';
import { getToken, handleUnauthorized } from './authService';
import type { EspecieData, Estadisticas } from '../../domain/models/estadistica';

export type { EspecieData, Estadisticas };

function getAuthHeaders(): HeadersInit {
  const token = getToken();
  if (!token) {
    handleUnauthorized();
    return { 'Content-Type': 'application/json' };
  }
  return {
    ...buildAuthHeaders(),
    'Authorization': `Bearer ${token}`,
  };
}

export async function obtenerEstadisticas(): Promise<Estadisticas> {
  const response = await fetch(`${API_BASE_URL}/estadisticas`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al obtener estadísticas');
  }

  return response.json();
}

