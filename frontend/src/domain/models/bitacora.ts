export interface Bitacora {
  id: number;
  mascota_id: number;
  fecha: string;
  tipo: string;
  descripcion: string;
  tratamiento?: string;
  medicamentos?: string;
  costo?: string;
  proxima_cita?: string;
}

export interface BitacoraCreate {
  tipo: string;
  descripcion: string;
  tratamiento?: string;
  medicamentos?: string;
  costo?: string;
  proxima_cita?: string;
}

