import type {
  LoginCredentials,
  LoginResponse,
  Veterinaria,
  VeterinariaRegistro,
} from '../../domain/models/auth';
import {
  login,
  registrarVeterinaria,
  saveSession,
} from '../../infrastructure/api/authService';

/**
 * Sanitiza la entrada de teléfono permitiendo únicamente números, +, - y espacios.
 */
export function sanitizePhoneInput(value: string): string {
  return value.replace(/[^0-9+\s\-]/g, '');
}

/**
 * Valida que el teléfono contenga exactamente 10 dígitos numéricos.
 */
export function validateRegistrationPhone(phone: string): boolean {
  const digitsOnly = phone.replace(/[^0-9]/g, '');
  return digitsOnly.length === 10;
}

/**
 * Valida que el correo tenga formato válido y termine en un dominio permitido.
 */
export function validateRegistrationEmail(email: string): boolean {
  const validDomains = [
    '.com',
    '.mx',
    '.org',
    '.net',
    '.edu',
    '.gov',
    '.io',
    '.co.mx',
    '.gob.mx',
    '.com.mx',
    '.edu.mx',
  ];
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) return false;
  return validDomains.some((domain) => email.toLowerCase().endsWith(domain));
}

/**
 * Caso de uso: Iniciar sesión y persistir la sesión activa.
 */
export async function iniciarSesionUseCase(
  credentials: LoginCredentials
): Promise<LoginResponse> {
  const email = credentials.email.trim().toLowerCase();
  const password = credentials.password;

  const response = await login({ email, password });

  if (response.success && response.token && response.veterinaria) {
    saveSession(response.token, response.veterinaria, response.usuario);
    return response;
  }

  throw new Error(response.message || 'Error al iniciar sesión');
}

/**
 * Caso de uso: Validar formulario de registro y crear una nueva veterinaria.
 */
export async function registrarVeterinariaUseCase(
  input: VeterinariaRegistro
): Promise<Veterinaria> {
  const telefono = input.telefono.trim();
  const email = input.email.trim().toLowerCase();

  if (!validateRegistrationPhone(telefono)) {
    throw new Error('El teléfono debe tener exactamente 10 dígitos numéricos');
  }

  if (!validateRegistrationEmail(email)) {
    throw new Error('El correo debe tener un dominio válido (ej: .com, .mx, .org)');
  }

  return registrarVeterinaria({
    nombre: input.nombre.trim(),
    telefono,
    direccion: input.direccion.trim(),
    email,
    password: input.password,
  });
}

