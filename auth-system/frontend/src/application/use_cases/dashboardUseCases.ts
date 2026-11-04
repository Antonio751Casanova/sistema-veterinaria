import type { TodoItem } from '../../domain/models/todo';

const TODO_KEY = 'vetpets_todo_list';

export const statusLabels: Record<string, string> = {
  pending: 'Pendiente',
  completed: 'Completada',
  cancelled: 'Cancelada',
};

export function formatTodoDate(dateStr: string): string {
  const d = new Date(dateStr);
  return (
    d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }) +
    ' ' +
    d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' })
  );
}

export function loadTodosUseCase(): TodoItem[] {
  try {
    const raw = localStorage.getItem(TODO_KEY);
    if (raw) {
      const items = JSON.parse(raw) as any[];
      let needsSave = false;
      for (const item of items) {
        if (!item.createdAt) {
          item.createdAt = new Date().toISOString();
          needsSave = true;
        }
        if (item.status === undefined) {
          item.status = item.completed ? 'completed' : 'pending';
          delete item.completed;
          needsSave = true;
        }
      }
      if (needsSave) saveTodosUseCase(items);
      return items;
    }
  } catch {}
  const now = new Date().toISOString();
  const defaults: TodoItem[] = [
    { id: 1, text: 'Llamar al proveedor de croquetas', status: 'completed', createdAt: now },
    { id: 2, text: 'Revisar inventario de vacunas', status: 'completed', createdAt: now },
    { id: 3, text: 'Confirmar citas del lunes', status: 'completed', createdAt: now },
    { id: 4, text: 'Limpiar área de gatos', status: 'pending', createdAt: now },
    { id: 5, text: 'Actualizar precios en sistema', status: 'pending', createdAt: now },
  ];
  saveTodosUseCase(defaults);
  return defaults;
}

export function saveTodosUseCase(todos: TodoItem[]): void {
  localStorage.setItem(TODO_KEY, JSON.stringify(todos));
}

