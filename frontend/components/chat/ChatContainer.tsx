'use client';

import React, { useRef, useEffect, useLayoutEffect } from 'react';
import { useChat } from '@/hooks/useChat';
import ChatMessage from '@/components/chat/ChatMessage';
import ChatInput from '@/components/chat/ChatInput';
import { ChatMessage as ChatMessageType } from '@/types/chat';
import NotificationProvider from '@/components/chat/NotificationProvider';

export default function ChatContainer() {
  const { messages, sendMessage, isLoading, error, setError } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({
        behavior,
        block: 'nearest'
      });
    }
  };

  useEffect(() => {
    // Scroll to bottom when messages change, with instant scroll for initial load
    const isInitialLoad = messages.length > 0 && messagesContainerRef.current?.scrollTop === 0;
    scrollToBottom(isInitialLoad ? 'instant' : 'smooth');
  }, [messages]);

  // Focus the input field when component mounts and when messages are loaded
  useLayoutEffect(() => {
    // Find the input element and focus it
    const input = document.querySelector('textarea[aria-label="Type your message"]') as HTMLTextAreaElement;
    if (input && !isLoading) {
      input.focus();
    }
  }, [messages, isLoading]); // Re-focus when messages change or loading state changes

  const handleSend = async (content: string) => {
    try {
      await sendMessage(content);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
    }
  };

  return (
    <NotificationProvider>
      <div className="flex flex-col h-[600px] border rounded-lg overflow-hidden bg-card shadow-md">
        <div className="bg-primary text-primary-foreground py-4 px-6">
          <h2 className="text-xl font-semibold">Todo Chat Assistant</h2>
        </div>

        <div
          ref={messagesContainerRef}
          className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[450px]"
        >
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
              <p>Start a conversation with the Todo Assistant!</p>
              <p className="text-sm mt-2">Try: "Add a task to buy groceries"</p>
            </div>
          ) : (
            messages.map((message: ChatMessageType) => (
              <ChatMessage key={message.id} message={message} />
            ))
          )}

          {isLoading && (
            <div className="flex items-center space-x-2 p-2 bg-secondary rounded-lg">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
              <span className="text-sm">Thinking...</span>
            </div>
          )}

          {error && (
            <div className="p-3 bg-destructive/10 border border-destructive rounded-lg text-destructive text-sm">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="border-t p-4 bg-muted">
          <ChatInput onSend={handleSend} disabled={isLoading} />
        </div>
      </div>
    </NotificationProvider>
  );
}