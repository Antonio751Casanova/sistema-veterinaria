import { API_BASE_URL } from '../config/api';
import type { Cita } from './citaService';

export interface ListaEsperaItem {
  id: number;
  tipo_atencion: string;
  duracion_minutos?: number;
  prioridad?: number;
  hora_inicio_preferida?: number;
  hora_fin_preferida?: number;
  notas?: string;
  preferencia_veterinario_id?: number;
  mascota_id: number;
  veterinaria_id: number;
  estado: string;
  fecha_creacion: string;
  nombre_mascota: string;
  especie_mascota: string;
  nombre_cliente: string;
  telefono_cliente: string;
  preferencia_veterinario_nombre?: string;
}

export interface ListaEsperaCreate {
  tipo_atencion: string;
  duracion_minutos?: number;
  prioridad?: number;
  hora_inicio_preferida?: number;
  hora_fin_preferida?: number;
  notas?: string;
  preferencia_veterinario_id?: number;
  mascota_id: number;
}

export interface ListaEsperaUpdate {
  tipo_atencion?: string;
  duracion_minutos?: number;
  prioridad?: number;
  hora_inicio_preferida?: number;
  hora_fin_preferida?: number;
  notas?: string;
  preferencia_veterinario_id?: number;
  estado?: string;
}

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

export async function listarListaEspera(estado?: string): Promise<ListaEsperaItem[]> {
  const url = new URL(`${API_BASE_URL}/lista-espera`);
  if (estado) {
    url.searchParams.set('estado', estado);
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al listar la lista de espera');
  }

  return response.json();
}

export async function obtenerItemListaEspera(id: number): Promise<ListaEsperaItem> {
  const response = await fetch(`${API_BASE_URL}/lista-espera/${id}`, {
    method: 'GET',
    headers: getAuthHeaders()
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
    body: JSON.stringify(data)
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
    body: JSON.stringify(data)
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
    headers: getAuthHeaders()
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
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error al convertir sugerencia en cita' }));
    throw new Error(error.detail || 'Error al convertir sugerencia en cita');
  }

  return response.json();
}
