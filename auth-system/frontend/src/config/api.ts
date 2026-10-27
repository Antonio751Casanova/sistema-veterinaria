// API Configuration
export const API_BASE_URL = 'http://localhost:8000';

// Auth / Veterinaria endpoints
export const AUTH_ENDPOINTS = {
  registro: `${API_BASE_URL}/veterinarias/registro`,
  login: `${API_BASE_URL}/veterinarias/login`,
  me: `${API_BASE_URL}/veterinarias/me`,
};

// Cliente endpoints
export const CLIENTE_ENDPOINTS = {
  base: `${API_BASE_URL}/clientes`,
  byId: (id: number) => `${API_BASE_URL}/clientes/${id}`,
  mascotas: (clienteId: number) => `${API_BASE_URL}/clientes/${clienteId}/mascotas`,
};

// Mascota endpoints
export const MASCOTA_ENDPOINTS = {
  base: `${API_BASE_URL}/mascotas`,
  byId: (id: number) => `${API_BASE_URL}/mascotas/${id}`,
  byCliente: (clienteId: number) => `${API_BASE_URL}/clientes/${clienteId}/mascotas`,
};

// Bitacora endpoints
export const BITACORA_ENDPOINTS = {
  byMascota: (mascotaId: number) => `${API_BASE_URL}/mascotas/${mascotaId}/bitacora`,
  delete: (mascotaId: number, entradaId: number) => `${API_BASE_URL}/mascotas/${mascotaId}/bitacora/${entradaId}`,
};

// Cita endpoints
export const CITA_ENDPOINTS = {
  base: `${API_BASE_URL}/citas`,
  byId: (id: number) => `${API_BASE_URL}/citas/${id}`,
  recordatorioWhatsapp: (id: number) => `${API_BASE_URL}/citas/${id}/recordatorio-whatsapp`,
  recordatorioEmail: (id: number) => `${API_BASE_URL}/citas/${id}/recordatorio-email`,
};

// Usuario endpoints (RBAC)
export const USUARIO_ENDPOINTS = {
  base: `${API_BASE_URL}/usuarios`,
  byId: (id: number) => `${API_BASE_URL}/usuarios/${id}`,
};

/**
 * Obtiene el token JWT almacenado en localStorage o cookies
 */
export function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null;

  let raw = localStorage.getItem('token');

  if (!raw && typeof document !== 'undefined' && document.cookie) {
    const match = document.cookie
      .split('; ')
      .find((row) => row.startsWith('token='));
    if (match) {
      raw = decodeURIComponent(match.split('=')[1] || '');
    }
  }

  if (!raw) return null;

  const cleaned = raw
    .replace(/^Bearer\s+/i, '')
    .trim()
    .replace(/^["']|["']$/g, '');

  if (!cleaned || cleaned === 'null' || cleaned === 'undefined') {
    return null;
  }

  return cleaned;
}

/**
 * Construye los headers estándar incluyendo Authorization: Bearer <token>
 */
export function buildAuthHeaders(): Record<string, string> {
  const token = getStoredToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}
