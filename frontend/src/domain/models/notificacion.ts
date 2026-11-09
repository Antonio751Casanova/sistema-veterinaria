export interface Notificacion {
  id: number;
  tipo: string;
  mensaje: string;
  leida: number;
  fecha_creacion: string;
  cita_id?: number;
  destinatario_usuario_id?: number;
}

