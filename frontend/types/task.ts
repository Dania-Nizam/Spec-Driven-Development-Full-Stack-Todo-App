export interface Task {
  id: string; // Required
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}