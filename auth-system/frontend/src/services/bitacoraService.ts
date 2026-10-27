import { BITACORA_ENDPOINTS } from '../config/api';
import { getToken } from './authService';

// ==================== Interfaces ====================

export interface Bitacora {
  id: number;
  mascota_id: number;
  fecha: string;
  tipo: string;
  descripcion: string;
  tratamiento?: string;
  medicamentos?: string;
  costo?: string;
  proxima_cita?: string;
}

export interface BitacoraCreate {
  tipo: string;
  descripcion: string;
  tratamiento?: string;
  medicamentos?: string;
  costo?: string;
  proxima_cita?: string;
}

// ==================== Helper ====================

function getAuthHeaders(): HeadersInit {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
}

// ==================== CRUD Functions ====================

/**
 * Crear una nueva entrada en la bitácora de una mascota
 */
export async function crearEntradaBitacora(mascotaId: number, data: BitacoraCreate): Promise<Bitacora> {
  const response = await fetch(BITACORA_ENDPOINTS.byMascota(mascotaId), {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al crear entrada de bitácora');
  }

  return response.json();
}

/**
 * Listar todas las entradas de bitácora de una mascota
 */
export async function listarBitacora(mascotaId: number): Promise<Bitacora[]> {
  const response = await fetch(BITACORA_ENDPOINTS.byMascota(mascotaId), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al obtener bitácora');
  }

  return response.json();
}

/**
 * Eliminar una entrada de bitácora
 */
export async function eliminarEntradaBitacora(mascotaId: number, entradaId: number): Promise<void> {
  const response = await fetch(BITACORA_ENDPOINTS.delete(mascotaId, entradaId), {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al eliminar entrada');
  }
}
