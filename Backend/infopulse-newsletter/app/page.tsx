"use client"

import { useState, Suspense } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Mail, TrendingUp, Filter, Sun, Moon, Menu, X, Twitter, Github, Linkedin, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { ThreeBackgroundWrapper } from "./components/three-background"
import { AIToolsPanel } from "./components/ai-tools-panel"
import { NewsModal } from "./components/news-modal"
import { AIImageCard } from "./components/ai-image-card"
import { useTheme } from "./components/theme-provider"

// Enhanced news data with AI image URLs
const newsData = [
  {
    id: 1,
    category: "Tech",
    headline: "AI Revolution Transforms Healthcare Industry Worldwide",
    summary:
      "New artificial intelligence systems are revolutionizing patient care and medical diagnosis across major hospitals, improving accuracy by 40% and reducing diagnosis time significantly.",
    content: "Full article content would go here with detailed information about the AI healthcare revolution...",
    timestamp: "2 hours ago",
    source: "techcrunch.com",
    color: "from-cyan-400 to-blue-500",
    categoryColor: "#00FFFF",
    aiImage: "/ai-healthcare-futuristic-medical.png",
  },
  {
    id: 2,
    category: "Business",
    headline: "Global Markets Surge on Economic Recovery Signals",
    summary:
      "Stock markets worldwide see significant gains as economic indicators point to sustained recovery and growth, with tech stocks leading the charge.",
    content: "Detailed analysis of global market trends and economic recovery indicators...",
    timestamp: "4 hours ago",
    source: "bloomberg.com",
    color: "from-green-400 to-emerald-500",
    categoryColor: "#10B981",
    aiImage: "/stock-market-growth.png",
  },
  {
    id: 3,
    category: "Politics",
    headline: "Climate Summit Reaches Historic Agreement on Carbon Goals",
    summary:
      "World leaders unite on ambitious climate targets, setting new standards for carbon reduction and renewable energy adoption by 2030.",
    content: "Comprehensive coverage of the climate summit agreements and their global implications...",
    timestamp: "6 hours ago",
    source: "reuters.com",
    color: "from-blue-400 to-indigo-500",
    categoryColor: "#EF4444",
    aiImage: "/climate-summit-renewable-energy.png",
  },
  {
    id: 4,
    category: "Sports",
    headline: "Championship Finals Break Global Viewership Records",
    summary:
      "The most-watched sporting event of the year delivers thrilling competition and record-breaking audience numbers across all platforms.",
    content: "Complete coverage of the championship finals and record-breaking viewership statistics...",
    timestamp: "8 hours ago",
    source: "espn.com",
    color: "from-orange-400 to-red-500",
    categoryColor: "#F97316",
    aiImage: "/championship-stadium-celebration.png",
  },
  {
    id: 5,
    category: "World",
    headline: "International Space Station Mission Achieves Breakthrough",
    summary:
      "Astronauts complete groundbreaking research mission, advancing our understanding of space exploration and potential Mars colonization.",
    content: "In-depth report on the space station mission and its implications for future space exploration...",
    timestamp: "10 hours ago",
    source: "nasa.gov",
    color: "from-purple-400 to-pink-500",
    categoryColor: "#8B5CF6",
    aiImage: "/space-station-earth-orbit.png",
  },
  {
    id: 6,
    category: "Local",
    headline: "Smart City Initiative Launches Advanced Transportation",
    summary:
      "New smart traffic systems and electric bus networks promise to reduce commute times by 30% and environmental impact significantly.",
    content: "Local news coverage of the smart city transportation initiative and its expected benefits...",
    timestamp: "12 hours ago",
    source: "localnews.com",
    color: "from-pink-400 to-rose-500",
    categoryColor: "#EC4899",
    aiImage: "/placeholder-ibr1o.png",
  },
]

const categories = ["Home", "Local", "Politics", "Business", "Tech", "World", "Sports"]
const trendingNews = newsData.slice(0, 5)

export default function InfoPulse() {
  const { theme, toggleTheme } = useTheme()
  const [activeTab, setActiveTab] = useState("Home")
  const [email, setEmail] = useState("")
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [selectedFilters, setSelectedFilters] = useState<string[]>([])
  const [isAIToolsOpen, setIsAIToolsOpen] = useState(false)
  const [selectedNews, setSelectedNews] = useState<any>(null)

  const handleFilterChange = (category: string, checked: boolean) => {
    if (checked) {
      setSelectedFilters([...selectedFilters, category])
    } else {
      setSelectedFilters(selectedFilters.filter((f) => f !== category))
    }
  }

  const filteredNews = activeTab === "Home" ? newsData : newsData.filter((news) => news.category === activeTab)

  return (
    <div
      className={`min-h-screen transition-all duration-500 ${
        theme === "dark" ? "bg-[#0e0e0e] text-white" : "bg-[#f5f5f5] text-gray-900"
      }`}
    >
      {/* 3D Background */}
      <Suspense
        fallback={
          <div
            className={`fixed inset-0 -z-10 ${
              theme === "dark"
                ? "bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900"
                : "bg-gradient-to-br from-gray-100 via-white to-gray-100"
            }`}
          />
        }
      >
        <ThreeBackgroundWrapper />
      </Suspense>

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
              {categories.map((category) => (
                <motion.button
                  key={category}
                  onClick={() => setActiveTab(category)}
                  className={`px-4 py-2 rounded-lg transition-all duration-300 relative ${
                    activeTab === category
                      ? theme === "dark"
                        ? "text-[#00FFFF]"
                        : "text-indigo-600"
                      : theme === "dark"
                        ? "text-gray-400 hover:text-white"
                        : "text-gray-600 hover:text-gray-900"
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {category}
                  {activeTab === category && (
                    <motion.div
                      className={`absolute bottom-0 left-0 right-0 h-0.5 ${
                        theme === "dark"
                          ? "bg-gradient-to-r from-[#00FFFF] to-[#FF00FF]"
                          : "bg-gradient-to-r from-indigo-600 to-purple-600"
                      }`}
                      layoutId="activeTab"
                      initial={false}
                      transition={{ type: "spring", stiffness: 500, damping: 30 }}
                    />
                  )}
                </motion.button>
              ))}
            </nav>

            {/* Controls */}
            <div className="flex items-center gap-4">
              {/* AI Tools Button */}
              <motion.button
                onClick={() => setIsAIToolsOpen(true)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all duration-300 ${
                  theme === "dark"
                    ? "bg-gradient-to-r from-[#FF00FF]/20 to-[#00FFFF]/20 text-[#FF00FF] hover:from-[#FF00FF]/30 hover:to-[#00FFFF]/30"
                    : "bg-gradient-to-r from-purple-100 to-indigo-100 text-purple-600 hover:from-purple-200 hover:to-indigo-200"
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Sparkles className="w-4 h-4" />
                AI Tools
              </motion.button>

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

            <motion.div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto" whileHover={{ scale: 1.02 }}>
              <Input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`flex-1 ${
                  theme === "dark"
                    ? "bg-gray-800/50 border-gray-700 text-white placeholder-gray-400 focus:border-[#00FFFF]"
                    : "bg-white/50 border-gray-300 text-gray-900 placeholder-gray-500 focus:border-indigo-500"
                } backdrop-blur-sm`}
              />
              <Button
                className={`${
                  theme === "dark"
                    ? "bg-gradient-to-r from-[#00FFFF] to-[#FF00FF] text-black hover:shadow-lg hover:shadow-cyan-500/25"
                    : "bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg hover:shadow-indigo-500/25"
                } font-semibold transition-all duration-300`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Mail className="w-4 h-4 mr-2" />
                Subscribe
              </Button>
            </motion.div>
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
              {filteredNews.map((news, index) => (
                <AIImageCard
                  key={news.id}
                  news={news}
                  index={index}
                  theme={theme}
                  onClick={() => setSelectedNews(news)}
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

      {/* AI Tools Panel */}
      <AIToolsPanel isOpen={isAIToolsOpen} onClose={() => setIsAIToolsOpen(false)} theme={theme} />

      {/* News Modal */}
      <NewsModal news={selectedNews} onClose={() => setSelectedNews(null)} theme={theme} />
    </div>
  )
}
