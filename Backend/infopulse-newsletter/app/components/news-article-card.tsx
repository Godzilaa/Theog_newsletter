"use client"

import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Clock, User } from "lucide-react"
import { type NewsArticle } from "@/lib/api"

interface NewsArticleCardProps {
  article: NewsArticle
  index: number
  onClick?: () => void
}

export function NewsArticleCard({ article, index, onClick }: NewsArticleCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
    >
      <Card
        className="h-full cursor-pointer overflow-hidden border-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm transition-all duration-300 hover:shadow-xl"
        onClick={onClick}
      >
        <div className="relative h-48 overflow-hidden">
          {/* Image placeholder */}
          <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900">
            <img
              src={`https://via.placeholder.com/400x200/1e40af/ffffff?text=${encodeURIComponent(article.title.slice(0, 30))}`}
              alt={article.title}
              className="h-full w-full object-cover"
            />
          </div>
        </div>

        <CardContent className="p-4 sm:p-6">
          {/* Headline */}
          <h3 className="line-clamp-2 text-lg font-semibold leading-tight text-gray-900 dark:text-white">
            {article.title}
          </h3>

          {/* Summary */}
          <p className="line-clamp-3 mt-2 text-sm text-gray-700 dark:text-gray-300">
            {article.description}
          </p>

          {/* Metadata */}
          <div className="mt-4 flex flex-wrap items-center justify-between text-xs text-gray-500">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                {article.published_at}
              </div>
              {article.author && (
                <div className="flex items-center gap-1">
                  <User className="h-4 w-4" />
                  {article.author}
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}
