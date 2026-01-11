"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { LogOut } from "lucide-react";

export default function Navbar() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const checkAuth = () => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  };

  useEffect(() => {
    // 1. Pehli dafa check karein
    checkAuth();

    // 2. Refresh ke baghair update ke liye event listener
    window.addEventListener("storage", checkAuth);
    const interval = setInterval(checkAuth, 1000); // Har second check karein (backup fix)

    return () => {
      window.removeEventListener("storage", checkAuth);
      clearInterval(interval);
    };
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setIsLoggedIn(false);
    router.push("/login");
    router.refresh(); // Force refresh for safety
  };

  return (
    <nav className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-50 shadow-sm">
      <div className="container mx-auto px-4 max-w-6xl flex items-center justify-between h-full">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-xl font-bold text-gray-900 tracking-tight">
            Todo <span className="text-indigo-600">App</span>
          </span>
        </Link>

        <div className="flex items-center gap-4">
          {isLoggedIn ? (
            <button 
              onClick={handleLogout}
              className="flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-xl font-bold hover:bg-red-100 transition-all border border-red-100"
            >
              <LogOut size={18} /> Logout
            </button>
          ) : (
            <Link 
              href="/login" 
              className="bg-indigo-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-indigo-700 transition-all"
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}