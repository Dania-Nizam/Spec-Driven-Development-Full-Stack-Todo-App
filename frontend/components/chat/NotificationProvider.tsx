'use client';

import React, { useEffect, ReactNode } from 'react';
import { useNotifications } from '@/hooks/useNotifications';

interface NotificationProviderProps {
  children: ReactNode;
}

export default function NotificationProvider({ children }: NotificationProviderProps) {
  const { permission, requestPermission } = useNotifications();

  useEffect(() => {
    // Automatically request permission when component mounts
    if (permission === 'default') {
      requestPermission();
    }
  }, [permission, requestPermission]);

  return (
    <>
      {children}
    </>
  );
}