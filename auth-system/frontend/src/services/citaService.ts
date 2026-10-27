import { API_BASE_URL } from '../config/api';

const APP_BASE_URL = 'http://localhost:4321';

export interface Cita {
  id: number;
  fecha_hora: string;
  duracion_minutos?: number;
  tipo_atencion: string;
  descripcion?: string;
  tratamiento?: string;
  medicamento?: string;
  costo?: string;
  estado: string;
  mascota_id: number;
  recordatorio_whatsapp_enviado: number;
  recordatorio_email_enviado: number;
  fecha_creacion: string;
}

export interface CitaConDetalles extends Cita {
  nombre_mascota: string;
  especie_mascota: string;
  nombre_cliente: string;
  telefono_cliente: string;
  email_cliente?: string;
  confirmation_token?: string;
  veterinario_asignado_id?: number;
  nombre_veterinario_asignado?: string;
}

export interface CitaCreate {
  fecha_hora: string;
  duracion_minutos?: number;
  tipo_atencion: string;
  mascota_id: number;
  descripcion?: string;
  tratamiento?: string;
  medicamento?: string;
  costo?: string;
  estado?: string;
  veterinario_asignado_id?: number;
}

export interface CitaUpdate {
  fecha_hora?: string;
  duracion_minutos?: number;
  tipo_atencion?: string;
  descripcion?: string;
  tratamiento?: string;
  medicamento?: string;
  costo?: string;
  estado?: string;
}

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

export async function listarCitas(): Promise<CitaConDetalles[]> {
  const response = await fetch(`${API_BASE_URL}/citas`, {
    method: 'GET',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al listar citas');
  }

  return response.json();
}

export async function obtenerCita(id: number): Promise<CitaConDetalles> {
  const response = await fetch(`${API_BASE_URL}/citas/${id}`, {
    method: 'GET',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al obtener cita');
  }

  return response.json();
}

export async function crearCita(data: CitaCreate): Promise<Cita> {
  const response = await fetch(`${API_BASE_URL}/citas`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al crear cita');
  }

  return response.json();
}

export async function actualizarCita(id: number, data: CitaUpdate): Promise<Cita> {
  const response = await fetch(`${API_BASE_URL}/citas/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al actualizar cita');
  }

  return response.json();
}

export async function eliminarCita(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/citas/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al eliminar cita');
  }
}

export async function marcarRecordatorioWhatsApp(id: number): Promise<Cita> {
  const response = await fetch(`${API_BASE_URL}/citas/${id}/recordatorio-whatsapp`, {
    method: 'PUT',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al marcar recordatorio');
  }

  return response.json();
}

export async function marcarRecordatorioEmail(id: number): Promise<Cita> {
  const response = await fetch(`${API_BASE_URL}/citas/${id}/recordatorio-email`, {
    method: 'PUT',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Error al marcar recordatorio');
  }

  return response.json();
}

export function generarMensajeWhatsApp(cita: CitaConDetalles): string {
  const fecha = new Date(cita.fecha_hora);
  const fechaFormateada = fecha.toLocaleDateString('es-MX', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  const horaFormateada = fecha.toLocaleTimeString('es-MX', {
    hour: '2-digit',
    minute: '2-digit'
  });

  const confirmacionLinks = cita.confirmation_token
    ? `\n\nPara *CONFIRMAR* su cita toque aqui:\n` +
      `${APP_BASE_URL}/confirmar-cita?confirmar=${cita.confirmation_token}` +
      `\n\nPara *CANCELAR* su cita toque aqui:\n` +
      `${APP_BASE_URL}/confirmar-cita?rechazar=${cita.confirmation_token}`
    : `\n\nPor favor, confirme su asistencia respondiendo a este mensaje.`;

  const mensaje = `Hola ${cita.nombre_cliente},

Le recordamos que tiene una cita programada para ${cita.nombre_mascota}:

Fecha: ${fechaFormateada}
Hora: ${horaFormateada}
Tipo de atencion: ${cita.tipo_atencion}${confirmacionLinks}

Gracias por confiar en nosotros.`;

  return mensaje;
}

export function generarMensajeEmail(cita: CitaConDetalles): { subject: string; body: string } {
  const fecha = new Date(cita.fecha_hora);
  const fechaFormateada = fecha.toLocaleDateString('es-MX', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  const horaFormateada = fecha.toLocaleTimeString('es-MX', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  
  const subject = `Recordatorio de cita para ${cita.nombre_mascota} - ${fechaFormateada}`;
  
  const body = `Estimado/a ${cita.nombre_cliente},

Le recordamos que tiene una cita programada para ${cita.nombre_mascota}.

Detalles de la cita:
- Fecha: ${fechaFormateada}
- Hora: ${horaFormateada}
- Tipo de atencion: ${cita.tipo_atencion}
${cita.descripcion ? `- Notas: ${cita.descripcion}` : ''}

Por favor, confirme su asistencia respondiendo a este correo.

Atentamente,
Veterinaria`;

  return { subject, body };
}

export function abrirWhatsApp(telefono: string, mensaje: string): void {
  const telefonoLimpio = telefono.replace(/\D/g, '');
  const url = `https://wa.me/${telefonoLimpio}?text=${encodeURIComponent(mensaje)}`;
  window.open(url, '_blank');
}

export function abrirEmail(email: string, subject: string, body: string): void {
  const url = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  window.open(url, '_blank');
}

// ==================== Confirmación pública (sin JWT — token ES la auth) ====================

export interface CitaConfirmacionPublicResponse {
  id: number;
  estado: string;
  fecha_hora: string;
  tipo_atencion: string;
  nombre_mascota: string;
  nombre_cliente: string;
  message: string;
}

export async function confirmarCitaPublic(token: string): Promise<CitaConfirmacionPublicResponse> {
  const response = await fetch(
    `${API_BASE_URL}/citas/confirmar?token=${encodeURIComponent(token)}`
    // Sin Authorization header — el token UUID es la autenticación
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || 'Error al confirmar la cita');
  }

  return response.json();
}

export async function rechazarCitaPublic(token: string): Promise<CitaConfirmacionPublicResponse> {
  const response = await fetch(
    `${API_BASE_URL}/citas/rechazar?token=${encodeURIComponent(token)}`
    // Sin Authorization header — el token UUID es la autenticación
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(error.detail || 'Error al cancelar la cita');
  }

  return response.json();
}
