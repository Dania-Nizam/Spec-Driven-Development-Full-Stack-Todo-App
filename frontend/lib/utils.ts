import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Utility functions for error handling and loading states
 */

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface LoadingStateType {
  state: LoadingState;
  message?: string;
  error?: string;
}

/**
 * Creates a loading state object
 */
export function createLoadingState(
  state: LoadingState,
  message?: string,
  error?: string
): LoadingStateType {
  return { state, message, error };
}

/**
 * Handles asynchronous operations with loading states
 */
export async function withLoadingState<T>(
  operation: () => Promise<T>,
  setLoading: (state: LoadingStateType) => void
): Promise<T> {
  try {
    setLoading(createLoadingState('loading', 'Processing...'));
    const result = await operation();
    setLoading(createLoadingState('success'));
    return result;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    setLoading(createLoadingState('error', undefined, errorMessage));
    throw error;
  }
}

/**
 * Validates message content according to requirements
 * - 1-2000 characters
 */
export function validateMessageContent(content: string): { isValid: boolean; error?: string } {
  if (!content || content.trim().length === 0) {
    return { isValid: false, error: 'Message cannot be empty' };
  }

  if (content.length > 2000) {
    return { isValid: false, error: 'Message exceeds 2000 characters limit' };
  }

  return { isValid: true };
}

/**
 * Sanitizes user input to prevent XSS
 */
export function sanitizeInput(input: string): string {
  // Basic sanitization to prevent simple XSS attempts
  return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
}

/**
 * Formats error messages for display
 */
export function formatErrorMessage(error: unknown): string {
  if (typeof error === 'string') {
    return error;
  }

  if (error instanceof Error) {
    return error.message;
  }

  if (error && typeof error === 'object' && 'message' in error) {
    return String((error as Record<string, unknown>).message);
  }

  return 'An unknown error occurred';
}

/**
 * Delays execution for a specified amount of time
 */
export function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}