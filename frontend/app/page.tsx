"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { Plus, AlertCircle, CheckCircle } from "lucide-react";
// 1. Sahi import use karein
import { authClient } from "@/lib/auth-client";
import { createApiClientWithAuth } from "@/lib/api-client";
import { isErrorResponse } from "@/lib/error-handler";
import Navbar from "./components/Navbar";
import TaskCard from "@/components/TaskCard";
import TaskModal from "@/components/TaskModal";

// 2. Apni shared type use karein
import { Task } from "@/types/task";

export default function DashboardPage() {
  // 3. authClient se session data lein
  const { data: session, isPending: authPending } = authClient.useSession();
  const user = session?.user;
  
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fabVisible, setFabVisible] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // ApiClient ko useMemo mein rakhein taaki unnecessary re-renders na hon
  const authApiClient = useMemo(() => createApiClientWithAuth(session), [session]);

  // Redirect logic
  useEffect(() => {
    if (!authPending && !user) {
      router.push('/login');
    }
  }, [authPending, user, router]);

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) return;

      try {
        setIsLoading(true);
        setError(null);

        const response = await authApiClient.get<Task[]>(`/api/${user.id}/tasks`);

        if (isErrorResponse(response)) {
          if (response.error === "unauthorized") {
            router.push('/login');
            return;
          }
          setError(response.error);
          return;
        }

        setTasks(response);
      } catch (err) {
        setError("Connection failed");
      } finally {
        setIsLoading(false);
      }
    };

    if (user && !authPending) {
      fetchTasks();
    }
  }, [user, authPending, authApiClient, router]);

  // Scroll logic for FAB
  useEffect(() => {
    const handleScroll = () => {
      setFabVisible(window.scrollY < 50);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  if (authPending) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading Session...</p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />

      <main className="pt-16 pb-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Welcome, {user.name || user.email}!
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Here's what you need to do today
            </p>
          </div>

          {error && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4 mb-6">
              <div className="flex">
                <AlertCircle className="h-5 w-5 text-red-400 mt-0.5" />
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800 dark:text-red-200">{error}</h3>
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {isLoading ? (
              // Skeletons
              Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="bg-white dark:bg-gray-800 p-4 rounded-lg animate-pulse h-32 border border-gray-200 dark:border-gray-700" />
              ))
            ) : tasks.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <CheckCircle className="mx-auto h-12 w-12 text-indigo-500 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">No tasks yet</h3>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md"
                >
                  <Plus className="mr-2 h-4 w-4" /> Create Task
                </button>
              </div>
            ) : (
              tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onTaskUpdate={(updatedTask) => {
                    setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
                  }}
                  onTaskDelete={(id) => {
                    setTasks(prev => prev.filter(t => t.id !== id));
                  }}
                />
              ))
            )}
          </div>
        </div>
      </main>

      {/* FABs */}
      <button
        onClick={() => setShowCreateModal(true)}
        className={`fixed bottom-6 right-6 p-4 bg-indigo-600 text-white rounded-full shadow-lg transition-all duration-300 ${
          fabVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
        } lg:hidden`}
      >
        <Plus className="h-6 w-6" />
      </button>

      <button
        onClick={() => setShowCreateModal(true)}
        className="hidden lg:flex fixed bottom-6 right-6 p-4 bg-indigo-600 text-white rounded-full shadow-lg"
      >
        <Plus className="h-6 w-6" />
      </button>

      <TaskModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSave={(newTask) => {
          setTasks(prev => [newTask, ...prev]);
          setShowCreateModal(false);
        }}
      />
    </div>
  );
}