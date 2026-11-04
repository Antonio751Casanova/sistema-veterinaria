export type RolUsuario = 'veterinario' | 'secretaria';

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: RolUsuario;
  activo: number;
}

export type UsuarioData = Usuario;

export interface UsuarioCreate {
  nombre: string;
  email: string;
  password: string;
  rol: RolUsuario;
}

