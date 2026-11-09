import type { Notificacion } from '../../domain/models/notificacion';

export interface NotificationTypeMeta {
  bg: string;
  color: string;
  label: string;
  icon: string;
}

export function getNotificationTypeMeta(tipo: string): NotificationTypeMeta {
  if (tipo === 'cita_asignada') return { bg: '#dbeafe', color: '#1d4ed8', label: 'Asignacion', icon: '📅' };
  if (tipo === 'recordatorio_cita') return { bg: '#fef3c7', color: '#92400e', label: 'Recordatorio', icon: '⏰' };
  if (tipo === 'lista_espera_sugerencia') return { bg: '#ede9fe', color: '#5b21b6', label: 'Lista de Espera', icon: '🧠' };
  return { bg: '#e2e8f0', color: '#475569', label: 'Sistema', icon: '🔔' };
}

export function extractFirstWaitlistId(message: string): number | null {
  const match = message.match(/LE#(\d+)/i);
  if (!match) return null;
  const parsed = parseInt(match[1], 10);
  return Number.isNaN(parsed) ? null : parsed;
}

export function formatRelativeDate(dateStr: string): string {
  const diffMs = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'ahora';
  if (mins < 60) return `hace ${mins} min`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `hace ${hrs} h`;
  const days = Math.floor(hrs / 24);
  if (days === 1) return 'ayer';
  return `${days} dias`;
}

export function filterNotificationsUseCase(
  notificationItems: Notificacion[],
  options: {
    filter: 'unread' | 'all';
    searchTerm: string;
    dateFilter: string;
    toDateKey: (date: Date) => string;
  }
): { unreadItems: Notificacion[]; visible: Notificacion[] } {
  const unreadItems = notificationItems.filter(n => n.leida === 0);
  const base = options.filter === 'unread' ? unreadItems : notificationItems;
  const term = options.searchTerm.trim().toLowerCase();

  const visible = base.filter(n => {
    const matchesText =
      !term ||
      n.mensaje.toLowerCase().includes(term) ||
      n.tipo.toLowerCase().includes(term);
    const matchesDate =
      !options.dateFilter ||
      options.toDateKey(new Date(n.fecha_creacion)) === options.dateFilter;
    return matchesText && matchesDate;
  });

  return { unreadItems, visible };
}
