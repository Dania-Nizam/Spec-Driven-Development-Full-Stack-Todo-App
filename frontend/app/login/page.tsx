"use client";

import { useState } from "react";
import { Eye, EyeOff, User, Mail, Lock } from "lucide-react";
import { authClient } from "@/lib/auth-client";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"signin" | "signup">("signin");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  // Form states
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    await authClient.signIn.email({
      email,
      password,
    }, {
      onRequest: () => setLoading(true),
      onResponse: () => setLoading(false),
      onSuccess: (ctx) => {
        // --- FIXED LOGIC ---
        // Better-Auth response mein data direct ctx.data mein hota hai
        const token = (ctx.data as any)?.access_token;
        if (token) {
          localStorage.setItem("token", token);
        }
        
        toast.success("Login successful!");
        // Dashboard par redirect
        router.push("/dashboard");
        router.refresh();
      },
      onError: (ctx) => {
        setLoading(false);
        toast.error(ctx.error.message || "Login failed");
      }
    });
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    await authClient.signUp.email({
      email,
      password,
      name,
    }, {
      onRequest: () => setLoading(true),
      onResponse: () => setLoading(false),
      onSuccess: () => {
        toast.success("Account created successfully! Please sign in.");
        setActiveTab("signin");
        // Clear signup fields
        setName("");
        setConfirmPassword("");
      },
      onError: (ctx) => {
        setLoading(false);
        toast.error(ctx.error.message || "Registration failed");
      }
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Welcome</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {activeTab === "signin" ? "Sign in to your account" : "Create a new account"}
            </p>
          </div>

          <div className="flex mb-8 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
            <button
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeTab === "signin" ? "bg-white dark:bg-gray-600 shadow-sm" : "text-gray-500"
              }`}
              onClick={() => setActiveTab("signin")}
            > Sign In </button>
            <button
              className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                activeTab === "signup" ? "bg-white dark:bg-gray-600 shadow-sm" : "text-gray-500"
              }`}
              onClick={() => setActiveTab("signup")}
            > Sign Up </button>
          </div>

          <form onSubmit={activeTab === "signin" ? handleSignIn : handleSignUp}>
            {activeTab === "signup" && (
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    type="text" value={name} onChange={(e) => setName(e.target.value)} required
                    className="w-full pl-10 pr-3 py-3 border rounded-lg dark:bg-gray-700 outline-none"
                    placeholder="John Doe"
                  />
                </div>
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
                  className="w-full pl-10 pr-3 py-3 border rounded-lg dark:bg-gray-700 outline-none"
                  placeholder="name@example.com"
                />
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password} onChange={(e) => setPassword(e.target.value)} required
                  className="w-full pl-10 pr-10 py-3 border rounded-lg dark:bg-gray-700 outline-none"
                  placeholder="••••••••"
                />
                <button
                  type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-gray-400"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {activeTab === "signup" && (
              <div className="mb-6">
                <label className="block text-sm font-medium mb-2">Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required
                    className="w-full pl-10 pr-10 py-3 border rounded-lg dark:bg-gray-700 outline-none"
                    placeholder="••••••••"
                  />
                </div>
              </div>
            )}

            <button
              type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg disabled:opacity-50 transition-all"
            >
              {loading ? "Processing..." : activeTab === "signin" ? "Sign In" : "Sign Up"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}