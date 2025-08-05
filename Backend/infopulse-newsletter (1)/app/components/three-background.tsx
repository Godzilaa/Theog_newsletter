
"use client"

import { useState, useEffect } from "react"
import { useTheme } from "./theme-provider"

export function ThreeBackground() {
  const { theme } = useTheme()
  const [particles, setParticles] = useState<JSX.Element[]>([])
  // Only generate random particles on client
  useEffect(() => {
    const arr = Array.from({ length: 50 }).map((_, i) => {
      return (
        <div
          key={i}
          className={`absolute w-1 h-1 rounded-full ${theme === "dark" ? "bg-cyan-400" : "bg-indigo-400"} opacity-20 animate-pulse`}
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            animationDuration: `${2 + Math.random() * 2}s`,
          }}
        />
      )
    })
    setParticles(arr)
  }, [theme])

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Animated gradient background */}
      <div
        className={`absolute inset-0 ${
          theme === "dark"
            ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
            : "bg-gradient-to-br from-gray-100 via-white to-gray-100"
        }`}
      />

      {/* Animated particles (client only) */}
      <div className="absolute inset-0">
        {particles}
      </div>

      {/* Floating orbs */}
      <div className="absolute inset-0">
        <div
          className={`absolute w-32 h-32 rounded-full ${
            theme === "dark"
              ? "bg-gradient-to-r from-cyan-400/10 to-purple-400/10"
              : "bg-gradient-to-r from-indigo-400/10 to-purple-400/10"
          } blur-xl animate-float-slow`}
          style={{ top: "20%", left: "10%" }}
        />
        <div
          className={`absolute w-24 h-24 rounded-full ${
            theme === "dark"
              ? "bg-gradient-to-r from-purple-400/10 to-pink-400/10"
              : "bg-gradient-to-r from-purple-400/10 to-pink-400/10"
          } blur-xl animate-float-medium`}
          style={{ top: "60%", right: "15%" }}
        />
        <div
          className={`absolute w-40 h-40 rounded-full ${
            theme === "dark"
              ? "bg-gradient-to-r from-pink-400/10 to-cyan-400/10"
              : "bg-gradient-to-r from-indigo-400/10 to-cyan-400/10"
          } blur-xl animate-float-fast`}
          style={{ bottom: "20%", left: "20%" }}
        />
      </div>

      {/* Grid pattern overlay */}
      <div
        className={`absolute inset-0 opacity-5 ${theme === "dark" ? "bg-grid-cyan" : "bg-grid-indigo"}`}
        style={{
          backgroundImage: `radial-gradient(circle, ${theme === "dark" ? "#00FFFF" : "#6366f1"} 1px, transparent 1px)`,
          backgroundSize: "50px 50px",
        }}
      />
    </div>
  )
}
