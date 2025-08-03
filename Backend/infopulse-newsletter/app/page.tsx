"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Sun, Moon, Menu, X, TrendingUp, Filter, Twitter, Github, Linkedin } from "lucide-react"
import { Switch } from "@/components/ui/switch"
import { NewsArticleCard } from "./components/news-article-card"
import { useTheme } from "./components/theme-provider"
import { CategoryNavbar } from "./components/category-navbar"
import { Badge } from "@/components/ui/badge"
import { type NewsArticle } from "@/lib/api"

// Enhanced news data with AI image URLs
const categories = ["technology", "business", "science", "health", "sports", "entertainment", "general"]

const newsData: NewsArticle[] = [
  {
    title: "AI Revolution Transforms Healthcare Industry",
    url: "https://techcrunch.com/ai-healthcare",
    description: "New artificial intelligence systems are revolutionizing patient care and medical diagnosis across major hospitals.",
    source: "TechCrunch",
    published_at: "2025-08-03T10:00:00Z",
    author: "John Doe",
    image_url: "/ai-healthcare.png"
  },
  {
    title: "Global Markets Surge on Economic Recovery",
    url: "https://bloomberg.com/markets",
    description: "Stock markets worldwide see significant gains as economic indicators point to sustained recovery and growth.",
    source: "Bloomberg",
    published_at: "2025-08-03T09:00:00Z",
    author: "Jane Smith",
    image_url: "/markets.png"
  },
  {
    title: "Space Station Research Breakthrough",
    url: "https://nasa.gov/news",
    description: "Astronauts complete groundbreaking research mission on the ISS.",
    source: "NASA",
    published_at: "2025-08-03T08:00:00Z",
    author: "Mike Johnson",
    image_url: "/space.png"
  }
]

// Top trending news
const trendingNews = newsData.slice(0, 5).map((article, index) => ({
  id: index,
  headline: article.title,
  category: categories[index % categories.length],
  color: index % 2 === 0 ? "from-cyan-500 to-blue-500" : "from-purple-500 to-pink-500",
  ...article
}))

export default function InfoPulse() {
  const { theme, toggleTheme } = useTheme()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [newsArticles] = useState<NewsArticle[]>(newsData)
  const [selectedNews, setSelectedNews] = useState<NewsArticle | null>(null)
  const [activeTab, setActiveTab] = useState(categories[0])
  const [selectedFilters, setSelectedFilters] = useState<string[]>([])

  const handleFilterChange = (category: string, checked: boolean) => {
    setSelectedFilters(prev => 
      checked ? [...prev, category] : prev.filter(c => c !== category)
    )
  }

  return (
    <div
      className={`min-h-screen transition-all duration-500 ${
        theme === "dark" ? "bg-[#0e0e0e] text-white" : "bg-[#f5f5f5] text-gray-900"
      }`}
    >
      {/* Background */}
      <div
        className={`fixed inset-0 -z-10 ${
          theme === "dark"
            ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
            : "bg-gradient-to-br from-gray-100 via-white to-gray-100"
        }`}
      />

      {/* Header */}
      <header
        className={`fixed top-0 w-full z-50 backdrop-blur-md transition-all duration-500 ${
          theme === "dark" ? "bg-[#0e0e0e]/80 border-gray-800" : "bg-[#f5f5f5]/80 border-gray-200"
        } border-b`}
      >
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <motion.div
              className="flex flex-col"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <motion.h1
                className={`text-3xl md:text-4xl font-bold transition-all duration-500 ${
                  theme === "dark"
                    ? "bg-gradient-to-r from-[#00FFFF] to-[#FF00FF] bg-clip-text text-transparent"
                    : "bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
                }`}
                whileHover={{
                  scale: 1.05,
                  textShadow: theme === "dark" ? "0 0 20px #00FFFF" : "0 0 20px #6366f1",
                }}
              >
                InfoPulse
              </motion.h1>
              <p
                className={`text-sm transition-colors duration-500 ${
                  theme === "dark" ? "text-gray-400" : "text-gray-600"
                }`}
              >
                Live-curated headlines powered by web scraping + AI
              </p>
            </motion.div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6">
              <CategoryNavbar />
            </nav>

            {/* Controls */}
            <div className="flex items-center gap-4">

              {/* Theme Toggle */}
              <motion.div className="flex items-center gap-2" whileHover={{ scale: 1.05 }}>
                <Sun
                  className={`w-4 h-4 transition-colors ${theme === "light" ? "text-yellow-500" : "text-gray-500"}`}
                />
                <Switch
                  checked={theme === "dark"}
                  onCheckedChange={toggleTheme}
                  className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-[#00FFFF] data-[state=checked]:to-[#FF00FF]"
                />
                <Moon className={`w-4 h-4 transition-colors ${theme === "dark" ? "text-blue-400" : "text-gray-500"}`} />
              </motion.div>

              {/* Mobile Menu Button */}
              <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          <AnimatePresence>
            {isMenuOpen && (
              <motion.nav
                className="md:hidden mt-4 pb-4"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="flex flex-col gap-2">
                  {categories.map((category) => (
                    <motion.button
                      key={category}
                      onClick={() => {
                        setActiveTab(category)
                        setIsMenuOpen(false)
                      }}
                      className={`px-4 py-2 rounded-lg text-left transition-all duration-300 ${
                        activeTab === category
                          ? theme === "dark"
                            ? "text-[#00FFFF] bg-[#00FFFF]/10"
                            : "text-indigo-600 bg-indigo-100"
                          : theme === "dark"
                            ? "text-gray-400 hover:text-white hover:bg-gray-800/50"
                            : "text-gray-600 hover:text-gray-900 hover:bg-gray-200"
                      }`}
                      whileHover={{ x: 5 }}
                    >
                      {category}
                    </motion.button>
                  ))}
                </div>
              </motion.nav>
            )}
          </AnimatePresence>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20">
        <div className="container mx-auto px-4 text-center z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <h2 className={`text-4xl md:text-6xl font-bold mb-6 ${theme === "dark" ? "text-white" : "text-gray-900"}`}>
              Get the News.{" "}
              <span
                className={`${
                  theme === "dark"
                    ? "bg-gradient-to-r from-[#00FFFF] to-[#FF00FF] bg-clip-text text-transparent"
                    : "bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
                }`}
              >
                Before the Noise.
              </span>
            </h2>

            <p className={`text-xl mb-8 ${theme === "dark" ? "text-gray-300" : "text-gray-600"}`}>
              Real-time news aggregation powered by AI and advanced web scraping
            </p>

            {/* Navigation Component */}
            <div className="mt-8">
              <CategoryNavbar />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* News Grid */}
          <main className="lg:col-span-3">
            <motion.div
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              {newsArticles.map((article, index) => (
                <NewsArticleCard
                  key={article.url}
                  article={article}
                  index={index}
                  onClick={() => setSelectedNews(article)}
                />
              ))}
            </motion.div>
          </main>

          {/* Sidebar */}
          <aside className="space-y-8">
            {/* Trending Headlines */}
            <motion.div
              className={`${
                theme === "dark" ? "bg-gray-900/50 border-gray-800" : "bg-white/50 border-gray-200"
              } backdrop-blur-sm rounded-xl p-6 border`}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <h3
                className={`text-xl font-bold mb-4 flex items-center ${
                  theme === "dark" ? "text-white" : "text-gray-900"
                }`}
              >
                <TrendingUp className={`w-5 h-5 mr-2 ${theme === "dark" ? "text-[#00FFFF]" : "text-indigo-600"}`} />
                Top 5 Trending
              </h3>
              <div className="space-y-3">
                {trendingNews.map((news, index) => (
                  <motion.div
                    key={news.id}
                    className={`p-3 rounded-lg transition-all duration-300 cursor-pointer ${
                      theme === "dark" ? "bg-gray-800/50 hover:bg-gray-800" : "bg-gray-100/50 hover:bg-gray-100"
                    }`}
                    whileHover={{ x: 5, scale: 1.02 }}
                    onClick={() => setSelectedNews(news)}
                  >
                    <div className="flex items-center mb-1">
                      <span className={`font-bold mr-2 ${theme === "dark" ? "text-[#00FFFF]" : "text-indigo-600"}`}>
                        #{index + 1}
                      </span>
                      <Badge className={`bg-gradient-to-r ${news.color} text-white border-0 text-xs`}>
                        {news.category}
                      </Badge>
                    </div>
                    <p className="text-sm font-medium line-clamp-2">{news.headline}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Category Filters */}
            <motion.div
              className={`${
                theme === "dark" ? "bg-gray-900/50 border-gray-800" : "bg-white/50 border-gray-200"
              } backdrop-blur-sm rounded-xl p-6 border`}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <h3
                className={`text-xl font-bold mb-4 flex items-center ${
                  theme === "dark" ? "text-white" : "text-gray-900"
                }`}
              >
                <Filter className={`w-5 h-5 mr-2 ${theme === "dark" ? "text-[#FF00FF]" : "text-purple-600"}`} />
                Category Filters
              </h3>
              <div className="space-y-3">
                {categories.slice(1).map((category) => (
                  <div key={category} className="flex items-center justify-between">
                    <label className="text-sm font-medium cursor-pointer">{category}</label>
                    <Switch
                      checked={selectedFilters.includes(category)}
                      onCheckedChange={(checked) => handleFilterChange(category, checked)}
                      className={`${
                        theme === "dark"
                          ? "data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-[#00FFFF] data-[state=checked]:to-[#FF00FF]"
                          : "data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-indigo-600 data-[state=checked]:to-purple-600"
                      }`}
                    />
                  </div>
                ))}
              </div>
            </motion.div>
          </aside>
        </div>
      </div>

      {/* Footer */}
      <footer
        className={`${
          theme === "dark" ? "bg-gray-900/50 border-gray-800" : "bg-white/50 border-gray-200"
        } backdrop-blur-sm border-t mt-16`}
      >
        <div className="container mx-auto px-4 py-12">
          <motion.div
            className="text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
          >
            <div className="flex justify-center gap-6 mb-6">
              {[
                { icon: Twitter, href: "#", color: "hover:text-blue-400" },
                { icon: Github, href: "#", color: "hover:text-gray-400" },
                { icon: Linkedin, href: "#", color: "hover:text-blue-600" },
              ].map(({ icon: Icon, href, color }, index) => (
                <motion.a
                  key={index}
                  href={href}
                  className={`p-3 rounded-full transition-all duration-300 ${
                    theme === "dark" ? "bg-gray-800 hover:bg-gray-700" : "bg-gray-100 hover:bg-gray-200"
                  } ${color}`}
                  whileHover={{
                    scale: 1.1,
                    boxShadow:
                      theme === "dark" ? "0 0 20px rgba(0, 255, 255, 0.3)" : "0 0 20px rgba(99, 102, 241, 0.3)",
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Icon className="w-5 h-5" />
                </motion.a>
              ))}
            </div>

            <div className="flex justify-center items-center gap-4 mb-4">
              <span className={`font-mono text-sm ${theme === "dark" ? "text-gray-400" : "text-gray-600"}`}>
                Powered by
              </span>
              <div className="flex items-center gap-2">
                <Badge className="bg-gradient-to-r from-pink-500 to-violet-500 text-white">DALL·E</Badge>
                <Badge className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white">Three.js</Badge>
                <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white">GPT</Badge>
              </div>
            </div>

            <p className={`font-mono text-sm ${theme === "dark" ? "text-gray-400" : "text-gray-600"}`}>
              Built with AI, Three.js, and caffeine ☕
            </p>
          </motion.div>
        </div>
      </footer>

    </div>
  )
}
