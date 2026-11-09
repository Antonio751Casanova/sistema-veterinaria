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

