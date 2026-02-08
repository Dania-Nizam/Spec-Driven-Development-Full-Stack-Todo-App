'use client';

import { useState, useEffect, useCallback } from 'react';
import { useAuth } from './useAuth';
import { chatApiClient } from '@/lib/api';

export interface Notification {
  id: string;
  userId: string;
  taskId: number;
  taskTitle: string;
  dueDatetime: string;
  timestamp: string;
  type: string;
}

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [permission, setPermission] = useState<NotificationPermission>('default');
  const { getUserInfo } = useAuth();

  // Check and request notification permission
  const requestPermission = useCallback(async () => {
    if (!('Notification' in window)) {
      console.log('This browser does not support desktop notifications');
      return;
    }

    const permission = await Notification.requestPermission();
    setPermission(permission);
    return permission;
  }, []);

  // Show browser notification
  const showBrowserNotification = useCallback((notification: Notification) => {
    if (permission !== 'granted') {
      console.log('Notification permission not granted');
      return;
    }

    const notificationOptions: NotificationOptions = {
      body: `Task "${notification.taskTitle}" is due soon!`,
      icon: '/favicon.ico',
      badge: '/favicon.ico',
      tag: `task-${notification.taskId}`,
      requireInteraction: true,
    };

    // Create notification
    const browserNotification = new Notification(`Due Soon: ${notification.taskTitle}`, notificationOptions);

    // Handle notification click
    browserNotification.onclick = (event) => {
      event.preventDefault();
      window.focus();
      // Could navigate to the task or chat interface
      console.log('Notification clicked for task:', notification.taskId);
    };
  }, [permission]);

  // Fetch user notifications from backend
  const fetchUserNotifications = useCallback(async () => {
    const userInfo = getUserInfo();
    if (!userInfo) {
      console.log('User not authenticated');
      return;
    }

    try {
      // We'll need to implement an API endpoint to fetch notifications
      // For now, we'll simulate by periodically checking for new notifications
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/${userInfo.userId}/notifications`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${userInfo.token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.notifications || [];
    } catch (error) {
      console.error('Error fetching notifications:', error);
      return [];
    }
  }, [getUserInfo]);

  // Poll for new notifications
  useEffect(() => {
    let pollInterval: NodeJS.Timeout;

    const startPolling = async () => {
      if (permission === 'granted') {
        try {
          const newNotifications = await fetchUserNotifications();

          // Filter out notifications that are already displayed
          const newUniqueNotifications = newNotifications.filter(
            (newNotif: Notification) =>
              !notifications.some(existingNotif => existingNotif.id === newNotif.id)
          );

          // Add new notifications to state
          if (newUniqueNotifications.length > 0) {
            setNotifications(prev => [...prev, ...newUniqueNotifications]);

            // Show browser notifications for each new notification
            newUniqueNotifications.forEach((notification: Notification) => {
              showBrowserNotification(notification);
            });
          }
        } catch (error) {
          console.error('Error polling notifications:', error);
        }
      }
    };

    // Start polling every 30 seconds
    pollInterval = setInterval(startPolling, 30000);

    // Initial check
    startPolling();

    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [permission, notifications, fetchUserNotifications, showBrowserNotification]);

  // Initialize notification permission on mount
  useEffect(() => {
    if ('Notification' in window) {
      setPermission(Notification.permission);

      // If permission is default, request it
      if (Notification.permission === 'default') {
        requestPermission();
      }
    }
  }, [requestPermission]);

  return {
    notifications,
    permission,
    requestPermission,
    showBrowserNotification,
    fetchUserNotifications,
  };
}