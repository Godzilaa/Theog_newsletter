"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Clock, ExternalLink, Sparkles } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"

interface AIImageCardProps {
  news: any
  index: number
  theme: string
  onClick: () => void
}

export function AIImageCard({ news, index, theme, onClick }: AIImageCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)

  return (
    <motion.article
      className={`${
        theme === "dark"
          ? "bg-gray-900/50 border-gray-800 hover:border-gray-700"
          : "bg-white/50 border-gray-200 hover:border-gray-300"
      } backdrop-blur-sm rounded-xl border transition-all duration-300 group cursor-pointer overflow-hidden`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{
        scale: 1.02,
        y: -5,
        boxShadow: theme === "dark" ? "0 20px 40px rgba(0, 255, 255, 0.1)" : "0 20px 40px rgba(99, 102, 241, 0.1)",
      }}
      onClick={onClick}
    >
      {/* AI-Generated Image */}
      <div className="relative h-48 overflow-hidden">
        {!imageLoaded && !imageError && (
          <div
            className={`absolute inset-0 ${
              theme === "dark" ? "bg-gray-800" : "bg-gray-200"
            } animate-pulse flex items-center justify-center`}
          >
            <div className="flex items-center gap-2 text-sm opacity-60">
              <Sparkles className="w-4 h-4 animate-spin" />
              Generating AI image...
            </div>
          </div>
        )}

        <motion.div
          className="relative w-full h-full"
          initial={{ scale: 1.1, opacity: 0 }}
          animate={{ scale: imageLoaded ? 1 : 1.1, opacity: imageLoaded ? 1 : 0 }}
          transition={{ duration: 0.6 }}
        >
          <Image
            src={news.aiImage || "/placeholder.svg"}
            alt={news.headline}
            fill
            className="object-cover transition-transform duration-300 group-hover:scale-105"
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageError(true)}
          />

          {/* AI Badge Overlay */}
          <motion.div
            className="absolute top-3 right-3 bg-gradient-to-r from-purple-500/90 to-pink-500/90 backdrop-blur-sm rounded-full px-2 py-1 flex items-center gap-1"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: imageLoaded ? 1 : 0, scale: imageLoaded ? 1 : 0.8 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Sparkles className="w-3 h-3 text-white" />
            <span className="text-xs text-white font-medium">AI</span>
          </motion.div>

          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
        </motion.div>
      </div>

      {/* Content */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-3">
          <Badge className={`bg-gradient-to-r ${news.color} text-white border-0 font-medium`}>{news.category}</Badge>
          <div
            className={`flex items-center text-sm font-mono ${theme === "dark" ? "text-gray-400" : "text-gray-500"}`}
          >
            <Clock className="w-4 h-4 mr-1" />
            {news.timestamp}
          </div>
        </div>

        <h2
          className={`text-xl font-bold mb-3 transition-colors duration-300 ${
            theme === "dark" ? "group-hover:text-[#00FFFF]" : "group-hover:text-indigo-600"
          }`}
        >
          {news.headline}
        </h2>

        <motion.p
          className={`mb-4 line-clamp-3 ${theme === "dark" ? "text-gray-300" : "text-gray-600"}`}
          initial={{ height: "3rem" }}
          whileHover={{ height: "auto" }}
          transition={{ duration: 0.3 }}
        >
          {news.summary}
        </motion.p>

        <div className="flex items-center justify-between">
          <span
            className={`text-sm font-mono flex items-center ${theme === "dark" ? "text-gray-500" : "text-gray-400"}`}
          >
            <ExternalLink className="w-3 h-3 mr-1" />
            {news.source}
          </span>
        </div>
      </div>
    </motion.article>
  )
}
