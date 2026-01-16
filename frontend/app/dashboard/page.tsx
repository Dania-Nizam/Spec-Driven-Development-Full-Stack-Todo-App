"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Trash2, CheckCircle2, Circle, Search, ClipboardList, Pencil, Calendar } from "lucide-react";

export default function Dashboard() {
  const router = useRouter();
  const [taskTitle, setTaskTitle] = useState("");
  const [priority, setPriority] = useState("Medium");
  const [dueDate, setDueDate] = useState(""); // 1. Due Date State
  const [filter, setFilter] = useState("All"); // 2. Tabs State
  const [todos, setTodos] = useState<any[]>([]);
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

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

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskTitle.trim()) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
      body: JSON.stringify({ 
        title: taskTitle, 
        description: "", 
        completed: false, 
        priority: priority,
        due_date: dueDate // Backend ko date bhejna
      })
    });
    if (res.ok) { 
      setTaskTitle(""); 
      setDueDate("");
      setPriority("Medium");
      fetchTodos(); 
      toast.success("Task Added!"); 
    }
  };

  const handleDelete = async (taskId: number) => {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) { fetchTodos(); toast.error("Task Deleted"); }
  };

  const handleToggle = async (taskId: number) => {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks/${taskId}/toggle`, {
      method: "PATCH",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (res.ok) fetchTodos();
  };

  const handleUpdate = async (taskId: number, currentTitle: string) => {
    const newTitle = prompt("Edit your task title:", currentTitle);
    if (newTitle === null || newTitle.trim() === "" || newTitle === currentTitle) return;
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
      body: JSON.stringify({ title: newTitle.trim(), description: "" })
    });
    if (res.ok) { fetchTodos(); toast.success("Task updated!"); }
  };

  // 3. LOGIC: Sorting & Filtering
  const priorityOrder: { [key: string]: number } = { High: 1, Medium: 2, Low: 3 };

  const filteredTodos = todos
    .filter(t => {
      const matchesSearch = t.title.toLowerCase().includes(searchQuery.toLowerCase());
      if (filter === "Pending") return matchesSearch && !t.completed;
      if (filter === "Completed") return matchesSearch && t.completed;
      return matchesSearch;
    })
    .sort((a, b) => (priorityOrder[a.priority] || 2) - (priorityOrder[b.priority] || 2));

  const progressPercent = todos.length > 0 ? Math.round((todos.filter(t => t.completed).length / todos.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#f8fafc] py-12 px-4 mt-16">
      <div className="max-w-2xl mx-auto">
        
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Today's Mission</h1>
            <p className="text-slate-500 font-medium">Manage your daily goals</p>
          </div>
        </div>

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

        {/* 4. UI: Status Tabs */}
        <div className="flex gap-2 mb-6 bg-slate-200/50 p-1.5 rounded-2xl w-fit">
          {["All", "Pending", "Completed"].map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${
                filter === tab ? "bg-white text-indigo-600 shadow-md" : "text-slate-500 hover:text-slate-700"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="space-y-4 mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-3.5 text-slate-400" size={18} />
            <input 
              type="text" placeholder="Search tasks..." value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-2xl outline-none focus:ring-2 ring-indigo-500 shadow-sm"
            />
          </div>
          
          <form onSubmit={handleAddTask} className="flex flex-col gap-3 bg-white p-4 rounded-3xl border border-slate-100 shadow-sm">
            <input 
              type="text" placeholder="What needs to be done?" value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              className="flex-1 px-4 py-2 text-lg font-medium outline-none"
            />
            <div className="flex flex-wrap gap-2 items-center border-t pt-3">
              <select 
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-600 outline-none"
              >
                <option value="Low">LOW</option>
                <option value="Medium">MEDIUM</option>
                <option value="High">HIGH</option>
              </select>

              <div className="flex items-center gap-2 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                <Calendar size={14} className="text-slate-400" />
                <input 
                  type="date" value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="bg-transparent text-xs font-bold text-slate-600 outline-none"
                />
              </div>

              <button className="ml-auto bg-indigo-600 text-white px-8 py-2 rounded-xl font-bold hover:bg-indigo-700 transition-all active:scale-95 shadow-lg shadow-indigo-200">
                Add Task
              </button>
            </div>
          </form>
        </div>

        <div className="space-y-3">
          {loading ? (
             <div className="text-center py-10 text-slate-400 animate-pulse">Loading tasks...</div>
          ) : filteredTodos.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-3xl border border-dashed border-slate-200">
              <p className="text-slate-400">No {filter.toLowerCase()} tasks found.</p>
            </div>
          ) : (
            filteredTodos.map((todo) => (
              <div key={todo.id} className="group bg-white p-4 rounded-2xl border border-slate-100 flex items-center justify-between shadow-sm hover:shadow-md transition-all">
                <div className="flex items-center gap-4 cursor-pointer flex-1" onClick={() => handleToggle(todo.id)}>
                  {todo.completed ? (
                    <CheckCircle2 className="text-green-500 flex-shrink-0" size={24} />
                  ) : (
                    <Circle className="text-slate-300 group-hover:text-indigo-400 flex-shrink-0" size={24} />
                  )}
                  
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className={`text-[9px] px-2 py-0.5 rounded-md font-black tracking-tighter uppercase ${
                        todo.priority === 'High' ? 'bg-red-100 text-red-600' : 
                        todo.priority === 'Medium' ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'
                      }`}>
                        {todo.priority}
                      </span>
                      {todo.due_date && (
                        <span className="text-[10px] text-slate-400 font-medium flex items-center gap-1">
                          <Calendar size={10} /> {todo.due_date}
                        </span>
                      )}
                    </div>
                    <span className={`text-base font-semibold transition-all ${todo.completed ? 'text-slate-300 line-through' : 'text-slate-700'}`}>
                      {todo.title}
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center gap-1">
                  <button onClick={(e) => { e.stopPropagation(); handleUpdate(todo.id, todo.title); }} className="p-2 text-slate-300 hover:text-indigo-600 rounded-xl transition-all">
                    <Pencil size={18} />
                  </button>
                  <button onClick={(e) => { e.stopPropagation(); handleDelete(todo.id); }} className="p-2 text-slate-300 hover:text-red-500 rounded-xl transition-all">
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}