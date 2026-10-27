import { USUARIO_ENDPOINTS, buildAuthHeaders } from '../config/api';
import { getToken, handleUnauthorized } from './authService';

export interface UsuarioData {
  id: number;
  nombre: string;
  email: string;
  rol: 'veterinario' | 'secretaria';
  activo: number;
}

export interface UsuarioCreate {
  nombre: string;
  email: string;
  password: string;
  rol: 'veterinario' | 'secretaria';
}

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

export async function listarUsuarios(): Promise<UsuarioData[]> {
  const response = await fetch(USUARIO_ENDPOINTS.base, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }
  if (!response.ok) throw new Error('Error al listar usuarios');
  return response.json();
}

export async function crearUsuario(data: UsuarioCreate): Promise<UsuarioData> {
  const response = await fetch(USUARIO_ENDPOINTS.base, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  });
  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Error al crear usuario');
  }
  return response.json();
}

export async function actualizarUsuario(id: number, data: UsuarioCreate): Promise<UsuarioData> {
  const response = await fetch(USUARIO_ENDPOINTS.byId(id), {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  });
  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Error al actualizar usuario');
  }
  return response.json();
}

export async function eliminarUsuario(id: number): Promise<void> {
  const response = await fetch(USUARIO_ENDPOINTS.byId(id), {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  if (response.status === 401) {
    handleUnauthorized();
    throw new Error('Sesión expirada. Por favor inicia sesión nuevamente.');
  }
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'Error al eliminar usuario');
  }
}

/** Obtener solo los veterinarios activos de la veterinaria (para selector en citas) */
export async function listarVeterinarios(): Promise<UsuarioData[]> {
  const todos = await listarUsuarios();
  return todos.filter(u => u.rol === 'veterinario' && u.activo === 1);
}
