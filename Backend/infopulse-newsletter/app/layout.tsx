import type React from "react"
import type { Metadata } from "next"
import { Sora } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "./components/theme-provider"

const sora = Sora({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "InfoPulse - AI-Powered News Visualization",
  description: "Live-curated headlines with AI-generated images and 3D visualization",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={sora.className}>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
