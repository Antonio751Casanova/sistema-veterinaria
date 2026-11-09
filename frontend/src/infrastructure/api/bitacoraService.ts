import { BITACORA_ENDPOINTS, buildAuthHeaders } from './api';
import { getToken, handleUnauthorized } from './authService';
import type { Bitacora, BitacoraCreate } from '../../domain/models/bitacora';

export type { Bitacora, BitacoraCreate };

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

export async function crearEntradaBitacora(mascotaId: number, data: BitacoraCreate): Promise<Bitacora> {
  const response = await fetch(BITACORA_ENDPOINTS.byMascota(mascotaId), {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Error al crear entrada de bitácora');
  }

  return response.json();
}

export async function listarBitacora(mascotaId: number): Promise<Bitacora[]> {
  const response = await fetch(BITACORA_ENDPOINTS.byMascota(mascotaId), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Error al obtener bitácora');
  }

  return response.json();
}

export async function eliminarEntradaBitacora(mascotaId: number, entradaId: number): Promise<void> {
  const response = await fetch(BITACORA_ENDPOINTS.delete(mascotaId, entradaId), {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Error al eliminar entrada');
  }
}

