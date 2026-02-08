import { useState, useCallback, useRef } from 'react';
import { chatApiClient } from '@/lib/api';
import { ChatMessage, ChatMessageSender, StreamChunk } from '@/types/chat';
import { v4 as uuidv4 } from 'uuid';
import { useAuth } from './useAuth';
import { validateMessageContent } from '@/lib/utils';

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { getUserInfo, isLoading: isAuthLoading } = useAuth();
  const currentBotMessageId = useRef<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    // Sabse pehle purana error saaf karein
    setError(null);

    // 1. Auth Loading Check
    if (isAuthLoading) {
      console.log("Waiting for auth to load...");
      return;
    }

    // 2. Auth & Redirect Logic (Fixed)
    const userInfo = getUserInfo();
    if (!userInfo) {
      setError("Please wait, verifying session...");
      // Foran bhagane ke bajaye 2 second ka gap dein taake session load ho sakay
      setTimeout(() => {
        if (!getUserInfo()) {
          window.location.href = '/login';
        } else {
          setError(null); // Agar mil gaya toh error hatayein
        }
      }, 2000);
      return;
    }

    try {
      // 3. Message validation
      const validation = validateMessageContent(content);
      if (!validation.isValid) {
        throw new Error(validation.error || 'Invalid message content');
      }

      setIsLoading(true);

      // 4. User message UI update
      const userMessageId = uuidv4();
      const userMessage: ChatMessage = {
        id: userMessageId,
        sessionId: 'default-session',
        content,
        sender: 'user' as ChatMessageSender,
        timestamp: new Date(),
        status: 'sent',
      };
      setMessages(prev => [...prev, userMessage]);

      // 5. Bot placeholder
      const botMessageId = uuidv4();
      currentBotMessageId.current = botMessageId;
      const initialBotMessage: ChatMessage = {
        id: botMessageId,
        sessionId: 'default-session',
        content: '',
        sender: 'bot' as ChatMessageSender,
        timestamp: new Date(),
        status: 'loading',
      };
      setMessages(prev => [...prev, initialBotMessage]);

      // 6. Regular API Call (not streaming)
      const response = await chatApiClient.sendMessage(
        userInfo.userId,
        content,
        undefined
      );

      // Update bot message with response
      setMessages(prev =>
        prev.map(msg =>
          msg.id === botMessageId
            ? {
                ...msg,
                content: response.response || 'No response',
                status: 'delivered',
                sessionId: response.session_id || msg.sessionId
              }
            : msg
        )
      );

    } catch (err) {
      console.error('Error sending message:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      if (currentBotMessageId.current) {
        setMessages(prev =>
          prev.map(msg =>
            msg.id === currentBotMessageId.current
              ? { ...msg, content: `Error: ${errorMessage}`, status: 'error' }
              : msg
          )
        );
      }
    } finally {
      setIsLoading(false);
      currentBotMessageId.current = null;
    }
  }, [getUserInfo, isAuthLoading]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    setError,
    clearMessages,
  };
}