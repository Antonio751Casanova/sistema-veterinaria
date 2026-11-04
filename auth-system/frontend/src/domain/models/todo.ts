export type TodoStatus = 'pending' | 'completed' | 'cancelled';

export interface TodoItem {
  id: number;
  text: string;
  status: TodoStatus;
  createdAt: string;
}

