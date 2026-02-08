export interface Task {
  id: number; // Backend returns integer
  title: string;
  description: string;
  completed: boolean;
  priority: string;
  due_date: string | null;
  user_id: number;
  created_at: string;
  updated_at: string;
}