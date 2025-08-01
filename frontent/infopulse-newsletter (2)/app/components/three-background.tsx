"use client"

import { useRef, useMemo, Suspense, useState, useEffect } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Points, PointMaterial } from "@react-three/drei"
import { useTheme } from "@/app/components/theme-provider"

function ParticleField() {
  const ref = useRef<any>()
  const { theme } = useTheme()

  const positions = useMemo(() => {
    const pos = new Float32Array(1000 * 3)
    for (let i = 0; i < 1000; i++) {
      // Generate random points in a sphere
      const radius = Math.random() * 1.5
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)

      pos[i * 3] = radius * Math.sin(phi) * Math.cos(theta)
      pos[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      pos[i * 3 + 2] = radius * Math.cos(phi)
    }
    return pos
  }, [])

  useFrame((state, delta) => {
    if (ref.current) {
      ref.current.rotation.x -= delta / 15
      ref.current.rotation.y -= delta / 20
    }
  })

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={positions} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color={theme === "dark" ? "#00FFFF" : "#6366f1"}
          size={0.002}
          sizeAttenuation={true}
          depthWrite={false}
          opacity={0.2}
        />
      </Points>
    </group>
  )
}

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

export function ThreeBackground() {
  const { theme } = useTheme()
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return <FallbackBackground theme={theme} />
  }

  return (
    <div className="fixed inset-0 -z-10">
      <Suspense fallback={<FallbackBackground theme={theme} />}>
        <Canvas
          dpr={[1, 2]}
          camera={{ position: [0, 0, 1] }}
          style={{ background: 'transparent' }}
        >
          <ParticleField />
        </Canvas>
      </Suspense>
    </div>
  )
}
