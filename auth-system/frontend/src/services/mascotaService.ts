import { MASCOTA_ENDPOINTS, CLIENTE_ENDPOINTS, buildAuthHeaders } from '../config/api';
import { getToken, handleUnauthorized } from './authService';

// ==================== Interfaces ====================

export interface Mascota {
  id: number;
  cliente_id: number;
  fecha_creacion: string;
  nombre: string;
  especie: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

export interface MascotaConDueno extends Mascota {
  nombre_dueno: string;
  telefono_dueno: string;
}

export interface MascotaCreate {
  nombre: string;
  especie: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

export interface MascotaUpdate {
  nombre?: string;
  especie?: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

// ==================== Helper ====================

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

// ==================== CRUD Functions ====================

/**
 * Crear una nueva mascota para un cliente
 */
export async function crearMascota(clienteId: number, data: MascotaCreate): Promise<Mascota> {
  const response = await fetch(CLIENTE_ENDPOINTS.mascotas(clienteId), {
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
    throw new Error(error.detail || 'Error al crear mascota');
  }

  return response.json();
}

/**
 * Listar todas las mascotas de la veterinaria
 */
export async function listarMascotas(): Promise<MascotaConDueno[]> {
  const response = await fetch(MASCOTA_ENDPOINTS.base, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Error al obtener mascotas');
  }

  return response.json();
}

/**
 * Listar mascotas de un cliente específico
 */
export async function listarMascotasCliente(clienteId: number): Promise<Mascota[]> {
  const response = await fetch(MASCOTA_ENDPOINTS.byCliente(clienteId), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Error al obtener mascotas del cliente');
  }

  return response.json();
}

/**
 * Obtener una mascota por ID
 */
export async function obtenerMascota(id: number): Promise<MascotaConDueno> {
  const response = await fetch(MASCOTA_ENDPOINTS.byId(id), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Mascota no encontrada');
  }

  return response.json();
}

/**
 * Actualizar una mascota
 */
export async function actualizarMascota(id: number, data: MascotaUpdate): Promise<Mascota> {
  const response = await fetch(MASCOTA_ENDPOINTS.byId(id), {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Error al actualizar mascota');
  }

  return response.json();
}

/**
 * Eliminar una mascota
 */
export async function eliminarMascota(id: number): Promise<void> {
  const response = await fetch(MASCOTA_ENDPOINTS.byId(id), {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Error al eliminar mascota');
  }
}
