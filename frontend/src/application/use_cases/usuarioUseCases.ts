import type {
  RolUsuario,
  UsuarioCreate,
  UsuarioData,
} from '../../domain/models/usuario';
import {
  actualizarUsuario,
  crearUsuario,
} from '../../infrastructure/api/usuarioService';

export const rolLabels: Record<string, string> = {
  veterinario: 'Veterinario',
  secretaria: 'Secretaria',
};

export const rolColors: Record<string, string> = {
  veterinario: 'background:#dbeafe;color:#1d4ed8;',
  secretaria: 'background:#dcfce7;color:#166534;',
};

export interface UsuarioFormInput {
  id?: string | number | null;
  nombre: string;
  email: string;
  password: string;
  rol: RolUsuario;
}

/**
 * Caso de uso: Validar y guardar (crear o actualizar) un usuario de la veterinaria.
 */
export async function guardarUsuarioUseCase(
  input: UsuarioFormInput
): Promise<UsuarioData> {
  const nombre = (input.nombre || '').trim();
  const email = (input.email || '').trim().toLowerCase();
  const password = input.password || '';
  const rol = input.rol;

  if (!nombre) {
    throw new Error('El nombre es obligatorio');
  }
  if (!email || !email.includes('@')) {
    throw new Error('Ingresa un correo electrónico válido');
  }

  const numericId =
    typeof input.id === 'number'
      ? input.id
      : input.id && String(input.id).trim()
      ? parseInt(String(input.id), 10)
      : null;

  if (!numericId && password.length < 6) {
    throw new Error('La contraseña debe tener al menos 6 caracteres');
  }

  const payload: UsuarioCreate = {
    nombre,
    email,
    password,
    rol,
  };

  if (numericId) {
    return actualizarUsuario(numericId, payload);
  }
  return crearUsuario(payload);
}

