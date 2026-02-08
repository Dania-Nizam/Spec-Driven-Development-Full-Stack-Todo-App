import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ReactNode } from "react";
import Navbar from "../components/Navbar";
import { Toaster } from "sonner";
// 1. AuthProvider ka import hata dein
// import { AuthProvider } from "./providers/auth-provider"; 

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Todo App",
  description: "A secure, multi-user todo application",
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {/* 2. <AuthProvider> wrapper ko yahan se delete karein */}
        <div className="min-h-screen bg-background">
          <Navbar />
          <main className="container mx-auto pt-16 pb-8 px-4 max-w-6xl">
            {children}
          </main>
        </div>
        <Toaster position="top-right" />
        {/* 3. Closing </AuthProvider> ko bhi hata dein */}
      </body>
    </html>
  );
}