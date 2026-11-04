import { API_BASE_URL, buildAuthHeaders } from './api';
import { getToken, handleUnauthorized } from './authService';
import type { Cita } from '../../domain/models/cita';
import type {
  ListaEsperaCreate,
  ListaEsperaItem,
  ListaEsperaUpdate,
} from '../../domain/models/listaEspera';

export type { ListaEsperaCreate, ListaEsperaItem, ListaEsperaUpdate };

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

export async function listarListaEspera(estado?: string): Promise<ListaEsperaItem[]> {
  const url = new URL(`${API_BASE_URL}/lista-espera`);
  if (estado) {
    url.searchParams.set('estado', estado);
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al listar la lista de espera');
  }

  return response.json();
}

export async function obtenerItemListaEspera(id: number): Promise<ListaEsperaItem> {
  const response = await fetch(`${API_BASE_URL}/lista-espera/${id}`, {
    method: 'GET',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Error al obtener elemento de lista de espera');
  }

  return response.json();
}

export async function crearItemListaEspera(data: ListaEsperaCreate): Promise<ListaEsperaItem> {
  const response = await fetch(`${API_BASE_URL}/lista-espera`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al crear elemento de lista de espera' }));
    throw new Error(error.detail || 'Error al crear elemento de lista de espera');
  }

  return response.json();
}

export async function actualizarItemListaEspera(id: number, data: ListaEsperaUpdate): Promise<ListaEsperaItem> {
  const response = await fetch(`${API_BASE_URL}/lista-espera/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al actualizar elemento de lista de espera' }));
    throw new Error(error.detail || 'Error al actualizar elemento de lista de espera');
  }

  return response.json();
}

export async function eliminarItemListaEspera(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/lista-espera/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al eliminar elemento de lista de espera' }));
    throw new Error(error.detail || 'Error al eliminar elemento de lista de espera');
  }
}

export async function convertirListaEsperaEnCita(params: {
  itemId: number;
  citaReferenciaId?: number;
  fechaHora?: string;
  veterinarioAsignadoId?: number;
}): Promise<Cita> {
  const { itemId, citaReferenciaId, fechaHora, veterinarioAsignadoId } = params;
  const url = new URL(`${API_BASE_URL}/lista-espera/${itemId}/convertir`);
  if (citaReferenciaId) {
    url.searchParams.set('cita_referencia_id', String(citaReferenciaId));
  }
  if (fechaHora) {
    url.searchParams.set('fecha_hora', fechaHora);
  }
  if (veterinarioAsignadoId) {
    url.searchParams.set('veterinario_asignado_id', String(veterinarioAsignadoId));
  }

  const response = await fetch(url.toString(), {
    method: 'POST',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al convertir sugerencia en cita' }));
    throw new Error(error.detail || 'Error al convertir sugerencia en cita');
  }

  return response.json();
}

