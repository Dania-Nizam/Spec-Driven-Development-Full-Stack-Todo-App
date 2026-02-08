
import React from 'react';
import { format } from 'date-fns';
import { cn } from '@/lib/utils';
import { ChatMessage as ChatMessageType } from '@/types/chat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user';
  const isError = message.status === 'error';
  const roleLabel = isUser ? 'user message' : 'assistant message';
  const statusLabel = message.status === 'delivered' ? '' : ` (${message.status})`;

  return (
    <div
      className={cn(
        'flex items-start gap-3',
        isUser ? 'justify-end' : 'justify-start'
      )}
      role="listitem"
      aria-label={`${roleLabel}${statusLabel}`}
    >
      {!isUser && !isError && (
        <div
          className="flex-shrink-0 flex items-center justify-center h-8 w-8 rounded-full bg-primary text-primary-foreground font-semibold text-sm"
          aria-label="Assistant avatar"
        >
          AI
        </div>
      )}

      {isError && (
        <div
          className="flex-shrink-0 flex items-center justify-center h-8 w-8 rounded-full bg-destructive text-destructive-foreground font-semibold text-sm"
          aria-label="Error indicator"
        >
          !
        </div>
      )}

      <div
        className={cn(
          'max-w-[75%] rounded-2xl px-4 py-2 text-sm shadow-sm',
          isUser && !isError
            ? 'bg-primary text-primary-foreground rounded-br-none ml-auto'
            : isError
            ? 'bg-destructive/10 border border-destructive rounded-none'
            : 'bg-secondary text-secondary-foreground rounded-bl-none'
        )}
        role="region"
        aria-live={isUser ? 'polite' : 'assertive'}
      >
        <div className={cn(
          "whitespace-pre-wrap break-words",
          isError ? 'text-destructive' : ''
        )}>
          {message.content}
        </div>

        <div className={cn(
          'text-xs mt-1 flex justify-between items-center',
          isError
            ? 'text-destructive'
            : isUser
              ? 'text-primary-foreground/70'
              : 'text-secondary-foreground/70'
        )}>
          <time dateTime={message.timestamp.toISOString()}>
            {format(message.timestamp, 'h:mm a')}
          </time>
          {message.status !== 'delivered' && (
            <span className="ml-2 text-xs capitalize" aria-label={`Status: ${message.status}`}>
              {message.status === 'loading' && 'Sending...'}
              {message.status === 'error' && 'Failed'}
              {message.status === 'sent' && 'Sent'}
            </span>
          )}
        </div>
      </div>

      {isUser && (
        <div
          className="flex-shrink-0 flex items-center justify-center h-8 w-8 rounded-full bg-secondary text-secondary-foreground font-semibold text-sm"
          aria-label="User avatar"
        >
          U
        </div>
      )}
    </div>
  );
}