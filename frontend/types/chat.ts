/**
 * TypeScript types for ChatSession and ChatMessage entities
 */

export type ChatSession = {
  id: string; // unique identifier for the session
  userId: string; // authenticated user ID from JWT
  createdAt: Date; // timestamp when session started
  updatedAt: Date; // timestamp of last activity
  isActive: boolean; // whether session is currently active
  metadata: Record<string, any>; // additional session data
};

export type ChatMessageSender = 'user' | 'bot';

export type ChatMessageStatus = 'sent' | 'delivered' | 'error' | 'loading';

export type ChatMessage = {
  id: string; // unique identifier for the message
  sessionId: string; // reference to parent ChatSession
  content: string; // message text content
  sender: ChatMessageSender; // identifies message origin
  timestamp: Date; // when message was sent/received
  status: ChatMessageStatus; // delivery status
  error?: string; // error message if status is 'error'
};

export type ChatResponse = {
  response: string; // The chatbot's response to the user's message
  sessionId: string; // Session identifier for maintaining conversation context
  taskId?: string; // Optional ID of any task created/modified by the message
  intent?: string; // Detected intent from the user's message (e.g., 'add_task', 'view_tasks', 'update_task')
};

export type StreamChunk = {
  chunk?: string;
  done?: boolean;
  finalResponse?: string;
};