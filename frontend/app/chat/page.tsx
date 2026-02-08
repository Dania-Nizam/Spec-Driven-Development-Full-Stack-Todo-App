"use client";
import React from 'react';
import dynamic from 'next/dynamic';
import { Suspense } from 'react';

// Dynamically import AuthGuard with no SSR to handle client-side authentication
const AuthGuard = dynamic(() => import('@/components/chat/AuthGuard'), {
  ssr: false,
  loading: () => (
    <div className="flex justify-center items-center min-h-[60vh]">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
  )
});

// Dynamically import ChatContainer
const ChatContainer = dynamic(() => import('@/components/chat/ChatContainer'), {
  ssr: false
});

export default function ChatPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Todo Chat Assistant</h1>
        {/* Optional: Add any additional header elements here */}
      </div>

      <Suspense fallback={
        <div className="flex justify-center items-center h-[600px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      }>
        <AuthGuard>
          <ChatContainer />
        </AuthGuard>
      </Suspense>

      {/* Informational note about OpenAI ChatKit */}
      <div className="mt-4 text-sm text-gray-500 text-center">
        Powered by custom chat interface with JWT authentication
      </div>
    </div>
  );
}