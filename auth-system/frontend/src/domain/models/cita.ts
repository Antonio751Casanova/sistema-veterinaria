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
  mascota_id?: number;
  descripcion?: string;
  tratamiento?: string;
  medicamento?: string;
  costo?: string;
  estado?: string;
  veterinario_asignado_id?: number;
}

export interface CitaConfirmacionPublicResponse {
  id: number;
  estado: string;
  fecha_hora: string;
  tipo_atencion: string;
  nombre_mascota: string;
  nombre_cliente: string;
  message: string;
}
