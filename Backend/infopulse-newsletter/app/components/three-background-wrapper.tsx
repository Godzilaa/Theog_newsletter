"use client"

import dynamic from "next/dynamic"
import { useTheme } from "./theme-provider"

function FallbackBackground({ theme }: { theme: string }) {
  return (
    <div
      className={`fixed inset-0 -z-10 ${
        theme === "dark"
          ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
          : "bg-gradient-to-br from-gray-100 via-white to-gray-100"
      }`}
    >
      <div className="absolute inset-0 opacity-20">
        <div
          className={`absolute top-1/4 left-1/4 w-2 h-2 rounded-full ${
            theme === "dark" ? "bg-cyan-400" : "bg-indigo-400"
          } animate-pulse`}
        />
        <div
          className={`absolute top-3/4 right-1/3 w-1 h-1 rounded-full ${
            theme === "dark" ? "bg-purple-400" : "bg-purple-500"
          } animate-pulse delay-1000`}
        />
        <div
          className={`absolute bottom-1/4 left-1/2 w-1.5 h-1.5 rounded-full ${
            theme === "dark" ? "bg-cyan-300" : "bg-indigo-300"
          } animate-pulse delay-2000`}
        />
      </div>
    </div>
  )
}

// Dynamically import the Three.js component with no SSR
const ThreeBackgroundDynamic = dynamic(
  () => import("./three-background").then((mod) => ({ default: mod.ThreeBackground })),
  {
    ssr: false,
    loading: () => {
      // eslint-disable-next-line react-hooks/rules-of-hooks
      const { theme } = useTheme()
      return <FallbackBackground theme={theme} />
    },
  }
)

export function ThreeBackgroundWrapper() {
  const { theme } = useTheme()
  
  return <ThreeBackgroundDynamic />
}
