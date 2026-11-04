import { API_BASE_URL, buildAuthHeaders } from './api';
import { getToken, handleUnauthorized } from './authService';
import type { Notificacion } from '../../domain/models/notificacion';

export type { Notificacion };

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

export async function listarNotificaciones(): Promise<Notificacion[]> {
  const response = await fetch(`${API_BASE_URL}/notificaciones`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al listar notificaciones');
  }

  return response.json();
}

export async function listarNotificacionesNoLeidas(): Promise<Notificacion[]> {
  const response = await fetch(`${API_BASE_URL}/notificaciones/no-leidas`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al listar notificaciones');
  }

  return response.json();
}

export async function marcarNotificacionLeida(id: number): Promise<Notificacion> {
  const response = await fetch(`${API_BASE_URL}/notificaciones/${id}/leer`, {
    method: 'PUT',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al marcar notificación');
  }

  return response.json();
}

export async function eliminarNotificacion(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/notificaciones/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al eliminar notificación');
  }
}

