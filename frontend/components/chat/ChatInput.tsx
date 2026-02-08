import React, { useState, KeyboardEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (content: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = () => {
    if (inputValue.trim() && !disabled) {
      onSend(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex items-end gap-2" role="form" aria-label="Chat message input">
      <Textarea
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message here..."
        disabled={disabled}
        className="resize-none min-h-[60px] max-h-32"
        aria-label="Type your message"
        aria-disabled={disabled}
        role="textbox"
        aria-multiline="true"
        rows={3}
      />
      <Button
        onClick={handleSubmit}
        disabled={!inputValue.trim() || disabled}
        className="mb-1 h-10 w-10 p-0 rounded-full"
        aria-label="Send message"
        aria-disabled={disabled || !inputValue.trim()}
      >
        <Send className="h-4 w-4" />
      </Button>
    </div>
  );
}