import { AUTH_ENDPOINTS, buildAuthHeaders, getStoredToken } from '../config/api';

// ==================== Interfaces ====================

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

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: 'veterinario' | 'secretaria';
  activo: number;
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

// ==================== JWT Validation Helper ====================

function isJwtExpired(token: string): boolean {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return true;
    const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    const payload = JSON.parse(jsonPayload);
    if (typeof payload.exp === 'number') {
      const nowSec = Math.floor(Date.now() / 1000);
      return payload.exp <= nowSec;
    }
    return false;
  } catch {
    return true;
  }
}

// ==================== Auth Functions ====================

export async function registrarVeterinaria(data: VeterinariaRegistro): Promise<Veterinaria> {
  const response = await fetch(AUTH_ENDPOINTS.registro, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Error al registrar');
  }

  return response.json();
}

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const response = await fetch(AUTH_ENDPOINTS.login, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || 'Login fallido');
  }

  return response.json();
}

export async function getVeterinariaActual(): Promise<Veterinaria> {
  const response = await fetch(AUTH_ENDPOINTS.me, {
    method: 'GET',
    headers: buildAuthHeaders(),
  });

  if (!response.ok) throw new Error('No autorizado');
  return response.json();
}

// ==================== Session Helpers ====================

export function saveSession(token: string, veterinaria: Veterinaria, usuario?: Usuario): void {
  const cleanToken = token.replace(/^Bearer\s+/i, '').trim();
  localStorage.setItem('token', cleanToken);
  localStorage.setItem('veterinaria', JSON.stringify(veterinaria));
  if (usuario) {
    localStorage.setItem('usuario', JSON.stringify(usuario));
  }
  if (typeof document !== 'undefined') {
    document.cookie = `token=${encodeURIComponent(cleanToken)}; path=/; max-age=86400; SameSite=Lax`;
  }
}

export function getToken(): string | null {
  const token = getStoredToken();
  if (!token) return null;
  if (isJwtExpired(token)) {
    clearSession();
    return null;
  }
  return token;
}

export function getVeterinaria(): Veterinaria | null {
  const data = localStorage.getItem('veterinaria');
  return data ? JSON.parse(data) : null;
}

export function getUsuario(): Usuario | null {
  const data = localStorage.getItem('usuario');
  return data ? JSON.parse(data) : null;
}

export function getUserRole(): 'veterinario' | 'secretaria' | null {
  return getUsuario()?.rol ?? null;
}

export function isSecretaria(): boolean {
  return getUserRole() === 'secretaria';
}

export function isVeterinario(): boolean {
  return getUserRole() === 'veterinario';
}

export function clearSession(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
    localStorage.removeItem('veterinaria');
    localStorage.removeItem('usuario');
  }
  if (typeof document !== 'undefined') {
    document.cookie = 'token=; path=/; max-age=0; SameSite=Lax';
  }
}

export function handleUnauthorized(): void {
  clearSession();
  if (typeof window !== 'undefined' && window.location.pathname !== '/') {
    window.location.href = '/';
  }
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function getVetName(): string | null {
  const vet = getVeterinaria();
  return vet?.nombre || null;
}

export function logout(): void {
  clearSession();
}
