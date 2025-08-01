"use client"

import { motion, AnimatePresence } from "framer-motion"
import { X, Clock, ExternalLink, Share2, Bookmark } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"

interface NewsModalProps {
  news: any
  onClose: () => void
  theme: string
}

export function NewsModal({ news, onClose, theme }: NewsModalProps) {
  if (!news) return null

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className={`${
            theme === "dark" ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
          } rounded-xl border shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden`}
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          transition={{ type: "spring", damping: 25, stiffness: 200 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-800">
            <div className="flex items-center gap-3">
              <Badge className={`bg-gradient-to-r ${news.color} text-white border-0`}>{news.category}</Badge>
              <div className={`flex items-center text-sm ${theme === "dark" ? "text-gray-400" : "text-gray-500"}`}>
                <Clock className="w-4 h-4 mr-1" />
                {news.timestamp}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Share2 className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="icon">
                <Bookmark className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={onClose}>
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-120px)]">
            {/* Image */}
            <div className="relative h-64 md:h-80">
              <Image src={news.aiImage || "/placeholder.svg"} alt={news.headline} fill className="object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
            </div>

            {/* Article Content */}
            <div className="p-6">
              <h1 className="text-2xl md:text-3xl font-bold mb-4">{news.headline}</h1>
              <p className={`text-lg mb-6 ${theme === "dark" ? "text-gray-300" : "text-gray-600"}`}>{news.summary}</p>
              <div className="prose prose-lg max-w-none">
                <p className={theme === "dark" ? "text-gray-300" : "text-gray-700"}>{news.content}</p>
              </div>

              {/* Source */}
              <div className="mt-8 pt-6 border-t border-gray-800">
                <div className="flex items-center justify-between">
                  <span
                    className={`text-sm font-mono flex items-center ${
                      theme === "dark" ? "text-gray-500" : "text-gray-400"
                    }`}
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Source: {news.source}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    className={
                      theme === "dark" ? "border-gray-700 hover:bg-gray-800" : "border-gray-300 hover:bg-gray-100"
                    }
                  >
                    Read Original
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}
