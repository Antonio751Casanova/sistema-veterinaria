import type { Cliente, ClienteCreate } from '../../domain/models/cliente';
import {
  actualizarCliente,
  crearCliente,
} from '../../infrastructure/api/clienteService';

export interface ValidationResult {
  valid: boolean;
  message: string;
}

export interface ParsedDireccion {
  calle: string;
  numero: string;
  colonia: string;
  municipio: string;
}

export interface ClienteFormInput {
  nombre: string;
  telefono: string;
  email?: string;
  calle: string;
  numero_domicilio: string;
  colonia: string;
  municipio: string;
}

/**
 * Formatea una fecha ISO al formato local es-MX (dd/mm/yyyy).
 */
export function formatClientDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-MX', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

/**
 * Valida el teléfono de un cliente (10 dígitos, inicia 2-9, no repetido ni secuencial).
 */
export function validateClientPhone(phone: string): ValidationResult {
  const digits = phone.replace(/\D/g, '');
  if (digits.length !== 10) {
    return { valid: false, message: 'El teléfono debe tener exactamente 10 dígitos' };
  }
  if (!/^[2-9]/.test(digits)) {
    return {
      valid: false,
      message: 'El teléfono no es válido (debe iniciar con un dígito entre 2 y 9)',
    };
  }
  if (/^(\d)\1{9}$/.test(digits)) {
    return {
      valid: false,
      message: 'El teléfono no es válido (no puede ser un número repetido)',
    };
  }
  if (digits === '1234567890' || digits === '0987654321') {
    return { valid: false, message: 'El teléfono no es válido' };
  }
  return { valid: true, message: '' };
}

/**
 * Valida el formato y TLD del correo electrónico de un cliente.
 */
export function validateClientEmail(email: string): ValidationResult {
  if (!email) return { valid: true, message: '' };
  email = email.trim().toLowerCase();
  const parts = email.split('@');
  if (parts.length !== 2) {
    return { valid: false, message: 'El correo debe contener exactamente un @' };
  }
  const [local, domain] = parts;
  if (local.length < 2) {
    return {
      valid: false,
      message: 'El correo no es válido (la parte antes del @ es muy corta)',
    };
  }
  if (!domain.includes('.')) {
    return {
      valid: false,
      message: 'El correo debe incluir un dominio válido (ej. gmail.com)',
    };
  }
  const domainParts = domain.split('.');
  const tld = domainParts[domainParts.length - 1];
  if (tld.length < 2) {
    return { valid: false, message: 'El correo tiene una extensión de dominio inválida' };
  }
  const validTlds = [
    'com', 'mx', 'org', 'net', 'edu', 'gov', 'io', 'co', 'info', 'biz', 'gob',
    'uk', 'es', 'ar', 'cl', 'gt', 'hn', 'ni', 'sv', 'cr', 'pa', 'do', 've',
    'pe', 'bo', 'py', 'uy', 'ec', 'cu', 'pr', 'us', 'ca', 'de', 'fr', 'it',
    'jp', 'br', 'ru',
  ];
  if (!validTlds.includes(tld)) {
    return {
      valid: false,
      message: `La extensión ".${tld}" no es reconocida. Usa por ejemplo .com, .mx, .org`,
    };
  }
  const pattern =
    /^[a-z0-9][a-z0-9._%+\-]{0,62}@[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)*\.[a-z]{2,}$/;
  if (!pattern.test(email)) {
    return { valid: false, message: 'El correo no tiene un formato válido' };
  }
  return { valid: true, message: '' };
}

/**
 * Construye y valida la dirección completa a partir de los 4 campos del formulario.
 */
export function buildClientDireccion(
  calle: string,
  numeroDomicilio: string,
  colonia: string,
  municipio: string
): { valid: boolean; direccion: string; message: string } {
  const c = (calle || '').trim();
  const n = (numeroDomicilio || '').trim();
  const col = (colonia || '').trim();
  const mun = (municipio || '').trim();

  if (!c || !n || !col || !mun) {
    return {
      valid: false,
      direccion: '',
      message:
        'Completa todos los campos de la dirección (calle, número, colonia y municipio)',
    };
  }

  return {
    valid: true,
    direccion: `Calle ${c} #${n}, Col. ${col}, ${mun}`,
    message: '',
  };
}

/**
 * Descompone una dirección almacenada ("Calle X #N, Col. Y, Z") en sus 4 campos.
 */
export function parseClientDireccion(direccion?: string): ParsedDireccion {
  if (!direccion) {
    return { calle: '', numero: '', colonia: '', municipio: '' };
  }
  const m = direccion.match(/^Calle\s+(.+?)\s+#([^,]+),\s*Col\.\s*([^,]+),\s*(.+)$/);
  if (m) {
    return {
      calle: m[1].trim(),
      numero: m[2].trim(),
      colonia: m[3].trim(),
      municipio: m[4].trim(),
    };
  }
  return { calle: direccion, numero: '', colonia: '', municipio: '' };
}

/**
 * Filtra la lista de clientes según el término y tipo de búsqueda.
 */
export function filterClientes(
  clients: Cliente[],
  searchTerm: string,
  searchType: string
): Cliente[] {
  const term = (searchTerm || '').trim();
  if (!term) return [...clients];

  const termLower = term.toLowerCase();
  return clients.filter((client) => {
    switch (searchType) {
      case 'id':
        return client.id.toString() === term;
      case 'nombre':
        return client.nombre.toLowerCase().includes(termLower);
      case 'telefono':
        return client.telefono.includes(term);
      default:
        return (
          client.id.toString() === term ||
          client.nombre.toLowerCase().includes(termLower) ||
          client.telefono.includes(term)
        );
    }
  });
}

/**
 * Caso de uso: Validar y guardar (crear o actualizar) un cliente.
 */
export async function guardarClienteUseCase(
  clientId: string | number | null | undefined,
  formInput: ClienteFormInput
): Promise<Cliente> {
  const dirResult = buildClientDireccion(
    formInput.calle,
    formInput.numero_domicilio,
    formInput.colonia,
    formInput.municipio
  );
  if (!dirResult.valid) {
    throw new Error(dirResult.message);
  }

  const data: ClienteCreate = {
    nombre: formInput.nombre.trim(),
    telefono: formInput.telefono.trim(),
    email: formInput.email?.toLowerCase().trim() || undefined,
    direccion: dirResult.direccion,
  };

  const phoneResult = validateClientPhone(data.telefono);
  if (!phoneResult.valid) {
    throw new Error(phoneResult.message);
  }

  const emailResult = validateClientEmail(data.email || '');
  if (!emailResult.valid) {
    throw new Error(emailResult.message);
  }

  const numericId =
    typeof clientId === 'number'
      ? clientId
      : clientId && String(clientId).trim()
      ? parseInt(String(clientId), 10)
      : null;

  if (numericId) {
    return actualizarCliente(numericId, data);
  }
  return crearCliente(data);
}

