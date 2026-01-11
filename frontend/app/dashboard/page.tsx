"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Trash2, CheckCircle2, Circle, Search, ClipboardList } from "lucide-react";

export default function Dashboard() {
  const router = useRouter();
  const [taskTitle, setTaskTitle] = useState("");
  const [todos, setTodos] = useState<any[]>([]);
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  // 1. Session & Token Logic
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return router.push("/login");
    try {
      const payload = JSON.parse(window.atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
      setUserId(payload.sub || payload.user_id);
    } catch (e) { router.push("/login"); }
  }, [router]);

  const fetchTodos = async () => {
    if (!userId) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) setTodos(await res.json());
    setLoading(false);
  };

  useEffect(() => { if (userId) fetchTodos(); }, [userId]);

  // 2. Add Task
  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskTitle.trim()) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
      body: JSON.stringify({ title: taskTitle, description: "", completed: false })
    });
    if (res.ok) { setTaskTitle(""); fetchTodos(); toast.success("Task Added"); }
  };

  // 3. Delete Task
  const handleDelete = async (taskId: number) => {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) { fetchTodos(); toast.error("Task Deleted"); }
  };

  // 4. Toggle Completion
  const handleToggle = async (taskId: number) => {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks/${taskId}/toggle`, {
      method: "PATCH",
      headers: { "Authorization": `Bearer ${token}` }
    });
    
    if (res.ok) {
      fetchTodos();
    } else {
      toast.error("Failed to update task");
    }
  };

  // 5. Progress Calculation
  const completedCount = todos.filter(t => t.completed).length;
  const progressPercent = todos.length > 0 ? Math.round((completedCount / todos.length) * 100) : 0;

  // 6. Search Filter
  const filteredTodos = todos.filter(t => t.title.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="min-h-screen bg-[#f8fafc] py-12 px-4 mt-16">
      <div className="max-w-2xl mx-auto">
        
        {/* Header Section - Cleaned up */}
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Dania's Tasks</h1>
          <p className="text-slate-500 font-medium">Manage your daily goals</p>
        </div>

        {/* Progress Card */}
        <div className="bg-indigo-600 rounded-3xl p-6 mb-8 text-white shadow-xl shadow-indigo-200">
          <div className="flex justify-between items-end mb-4">
            <div>
              <p className="text-indigo-100 text-sm font-medium">Daily Progress</p>
              <h2 className="text-2xl font-bold">{progressPercent}% Completed</h2>
            </div>
            <ClipboardList size={32} className="opacity-50" />
          </div>
          <div className="w-full bg-indigo-400/30 rounded-full h-2.5">
            <div className="bg-white h-2.5 rounded-full transition-all duration-500" style={{ width: `${progressPercent}%` }}></div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-3.5 text-slate-400" size={18} />
            <input 
              type="text" placeholder="Search tasks..." value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 ring-indigo-500 shadow-sm"
            />
          </div>
          <form onSubmit={handleAddTask} className="flex gap-2">
            <input 
              type="text" placeholder="Add new task..." value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              className="flex-1 px-4 py-3 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 ring-indigo-500 shadow-sm"
            />
            <button className="bg-indigo-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-indigo-700 shadow-lg shadow-indigo-100 transition-all active:scale-95">Add</button>
          </form>
        </div>

        {/* Task List */}
        <div className="space-y-3">
          {loading ? (
             <div className="text-center py-10 text-slate-400 animate-pulse">Loading tasks...</div>
          ) : filteredTodos.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-3xl border border-dashed border-slate-200">
              <p className="text-slate-400">No tasks found. Start by adding one!</p>
            </div>
          ) : (
            filteredTodos.map((todo) => (
              <div key={todo.id} className="group bg-white p-4 rounded-2xl border border-slate-100 flex items-center justify-between shadow-sm hover:shadow-md transition-all">
                <div className="flex items-center gap-4 cursor-pointer" onClick={() => handleToggle(todo.id)}>
                  {todo.completed ? (
                    <CheckCircle2 className="text-green-500" size={24} />
                  ) : (
                    <Circle className="text-slate-300 group-hover:text-indigo-400" size={24} />
                  )}
                  <span className={`text-lg font-semibold transition-all ${todo.completed ? 'text-slate-300 line-through' : 'text-slate-700'}`}>
                    {todo.title}
                  </span>
                </div>
                <button 
                  onClick={() => handleDelete(todo.id)}
                  className="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all"
                >
                  <Trash2 size={20} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}