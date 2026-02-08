import { authClient } from './auth-client';

/**
 * API client for chat functionality
 */
export class ChatAPIClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  /**
   * Send a message to the chat endpoint (Normal POST)
   */
  async sendMessage(userId: string, message: string, sessionId?: string, retries = 3): Promise<any> {
    try {
      // Get access_token from cookies (this is the JWT)
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('access_token='))
        ?.split('=')[1];

      if (!token) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        credentials: 'include',

        body: JSON.stringify({
          message,
          sessionId: sessionId || undefined
        }),
      });

      if (response.status === 401) {
        await authClient.signOut();
        throw new Error('Session expired. Please log in again.');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        if ((response.status >= 500 || response.status === 429) && retries > 0) {
          await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
          return await this.sendMessage(userId, message, sessionId, retries - 1);
        }
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError && retries > 0) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
        return await this.sendMessage(userId, message, sessionId, retries - 1);
      }
      throw error;
    }
  }

  /**
   * Send a message with streaming support
   */
  async sendMessageStream(
    userId: string,
    message: string,
    sessionId?: string,
    onChunk?: (chunk: any) => void,
    retries = 3
  ): Promise<void> {
    try {
      // Get access_token from cookies (this is the JWT)
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('access_token='))
        ?.split('=')[1];

      if (!token) {
        throw new Error('User not authenticated');
      }

      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        credentials: 'include',

        body: JSON.stringify({
          message,
          sessionId: sessionId || undefined
        }),
      });

      if (response.status === 401) {
        await authClient.signOut();
        throw new Error('Session expired. Please log in again.');
      }

      if (!response.ok) {
        if ((response.status >= 500 || response.status === 429) && retries > 0) {
          await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
          return await this.sendMessageStream(userId, message, sessionId, onChunk, retries - 1);
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // FIX: Null check for response body reader
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Could not get response reader');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('data: ')) {
              try {
                const data = JSON.parse(trimmedLine.substring(6));
                if (onChunk) onChunk(data);
              } catch (e) {
                console.error('Error parsing SSE data:', e);
              }
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      if (error instanceof TypeError && retries > 0) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
        return await this.sendMessageStream(userId, message, sessionId, onChunk, retries - 1);
      }
      throw error;
    }
  }
}

export const chatApiClient = new ChatAPIClient();