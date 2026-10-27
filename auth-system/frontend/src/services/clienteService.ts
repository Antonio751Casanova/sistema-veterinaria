import { CLIENTE_ENDPOINTS, buildAuthHeaders } from '../config/api';
import { getToken, handleUnauthorized } from './authService';

// ==================== Interfaces ====================

export interface Cliente {
  id: number;
  veterinaria_id: number;
  fecha_creacion: string;
  nombre: string;
  telefono: string;
  email?: string;
  direccion?: string;
  total_mascotas: number;
}

export interface ClienteCreate {
  nombre: string;
  telefono: string;
  email?: string;
  direccion?: string;
}

export interface ClienteUpdate {
  nombre?: string;
  telefono?: string;
  email?: string;
  direccion?: string;
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
 * Crear un nuevo cliente (dueño)
 */
export async function crearCliente(data: ClienteCreate): Promise<Cliente> {
  const response = await fetch(CLIENTE_ENDPOINTS.base, {
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
    throw new Error(error.detail || 'Error al crear cliente');
  }

  return response.json();
}

/**
 * Listar todos los clientes
 */
export async function listarClientes(): Promise<Cliente[]> {
  const response = await fetch(CLIENTE_ENDPOINTS.base, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Error al obtener clientes');
  }

  return response.json();
}

/**
 * Obtener un cliente por ID
 */
export async function obtenerCliente(id: number): Promise<Cliente> {
  const response = await fetch(CLIENTE_ENDPOINTS.byId(id), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Cliente no encontrado');
  }

  return response.json();
}

/**
 * Actualizar un cliente
 */
export async function actualizarCliente(id: number, data: ClienteUpdate): Promise<Cliente> {
  const response = await fetch(CLIENTE_ENDPOINTS.byId(id), {
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
    throw new Error(error.detail || 'Error al actualizar cliente');
  }

  return response.json();
}

/**
 * Eliminar un cliente
 */
export async function eliminarCliente(id: number): Promise<void> {
  const response = await fetch(CLIENTE_ENDPOINTS.byId(id), {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }

  if (!response.ok) {
    throw new Error('Error al eliminar cliente');
  }
}
