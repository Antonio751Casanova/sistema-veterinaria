import type { Usuario } from './usuario';

export interface VeterinariaRegistro {
  nombre: string;
  telefono: string;
  direccion: string;
  email: string;
  password: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface Veterinaria {
  id: number;
  nombre: string;
  telefono: string;
  direccion: string;
  email: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  token?: string;
  veterinaria?: Veterinaria;
  usuario?: Usuario;
}

export interface ApiError {
  detail: string;
}

