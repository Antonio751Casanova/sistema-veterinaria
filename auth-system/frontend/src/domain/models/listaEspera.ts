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

