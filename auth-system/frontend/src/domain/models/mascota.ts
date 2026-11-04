export interface Mascota {
  id: number;
  cliente_id: number;
  fecha_creacion: string;
  nombre: string;
  especie: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

export interface MascotaConDueno extends Mascota {
  nombre_dueno: string;
  telefono_dueno: string;
}

export interface MascotaCreate {
  nombre: string;
  especie: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

export interface MascotaUpdate {
  nombre?: string;
  especie?: string;
  raza?: string;
  edad?: string;
  peso?: string;
  notas?: string;
}

