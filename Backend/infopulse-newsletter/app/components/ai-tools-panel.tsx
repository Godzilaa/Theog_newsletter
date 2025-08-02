"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { X, Sparkles, ImageIcon, MessageSquare, Lightbulb, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

interface AIToolsPanelProps {
  isOpen: boolean
  onClose: () => void
  theme: string
}

export function AIToolsPanel({ isOpen, onClose, theme }: AIToolsPanelProps) {
  const [activeTab, setActiveTab] = useState("image")
  const [imagePrompt, setImagePrompt] = useState("")
  const [summaryText, setSummaryText] = useState("")
  const [explainText, setExplainText] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerateImage = async () => {
    setIsGenerating(true)
    // Simulate AI image generation
    setTimeout(() => {
      setIsGenerating(false)
      // In a real app, this would call DALL-E API
    }, 3000)
  }

  const handleSummarize = async () => {
    setIsGenerating(true)
    // Simulate AI summarization
    setTimeout(() => {
      setIsGenerating(false)
      setSummaryText("AI-generated summary would appear here...")
    }, 2000)
  }

  const handleExplain = async () => {
    setIsGenerating(true)
    // Simulate AI explanation
    setTimeout(() => {
      setIsGenerating(false)
      setExplainText("Simple explanation would appear here...")
    }, 2000)
  }

  const tabs = [
    { id: "image", label: "Generate Image", icon: ImageIcon },
    { id: "summarize", label: "Summarize", icon: MessageSquare },
    { id: "explain", label: "Explain Like I'm 5", icon: Lightbulb },
  ]

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            className={`fixed right-0 top-0 h-full w-full max-w-md z-50 ${
              theme === "dark" ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
            } border-l shadow-2xl`}
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-800">
              <div className="flex items-center gap-3">
                <div
                  className={`p-2 rounded-lg ${
                    theme === "dark"
                      ? "bg-gradient-to-r from-[#FF00FF]/20 to-[#00FFFF]/20"
                      : "bg-gradient-to-r from-purple-100 to-indigo-100"
                  }`}
                >
                  <Sparkles className={`w-5 h-5 ${theme === "dark" ? "text-[#FF00FF]" : "text-purple-600"}`} />
                </div>
                <h2 className="text-xl font-bold">AI Tools</h2>
              </div>
              <Button variant="ghost" size="icon" onClick={onClose}>
                <X className="w-5 h-5" />
              </Button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-800">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 flex items-center justify-center gap-2 p-4 text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? theme === "dark"
                        ? "text-[#00FFFF] border-b-2 border-[#00FFFF]"
                        : "text-indigo-600 border-b-2 border-indigo-600"
                      : theme === "dark"
                        ? "text-gray-400 hover:text-white"
                        : "text-gray-600 hover:text-gray-900"
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="flex-1 p-6 overflow-y-auto">
              {activeTab === "image" && (
                <motion.div
                  className="space-y-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div>
                    <label className="block text-sm font-medium mb-2">Image Prompt</label>
                    <Textarea
                      placeholder="Describe the image you want to generate..."
                      value={imagePrompt}
                      onChange={(e) => setImagePrompt(e.target.value)}
                      className={`${
                        theme === "dark"
                          ? "bg-gray-800 border-gray-700 text-white"
                          : "bg-gray-50 border-gray-300 text-gray-900"
                      }`}
                      rows={4}
                    />
                  </div>
                  <Button
                    onClick={handleGenerateImage}
                    disabled={isGenerating || !imagePrompt.trim()}
                    className={`w-full ${
                      theme === "dark"
                        ? "bg-gradient-to-r from-[#FF00FF] to-[#00FFFF] text-black"
                        : "bg-gradient-to-r from-purple-600 to-indigo-600 text-white"
                    }`}
                  >
                    {isGenerating ? (
                      <>
                        <Zap className="w-4 h-4 mr-2 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <ImageIcon className="w-4 h-4 mr-2" />
                        Generate Image
                      </>
                    )}
                  </Button>
                </motion.div>
              )}

              {activeTab === "summarize" && (
                <motion.div
                  className="space-y-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div>
                    <label className="block text-sm font-medium mb-2">Text to Summarize</label>
                    <Textarea
                      placeholder="Paste the text you want to summarize..."
                      className={`${
                        theme === "dark"
                          ? "bg-gray-800 border-gray-700 text-white"
                          : "bg-gray-50 border-gray-300 text-gray-900"
                      }`}
                      rows={6}
                    />
                  </div>
                  <Button
                    onClick={handleSummarize}
                    disabled={isGenerating}
                    className={`w-full ${
                      theme === "dark"
                        ? "bg-gradient-to-r from-[#00FFFF] to-[#FF00FF] text-black"
                        : "bg-gradient-to-r from-indigo-600 to-purple-600 text-white"
                    }`}
                  >
                    {isGenerating ? (
                      <>
                        <Zap className="w-4 h-4 mr-2 animate-spin" />
                        Summarizing...
                      </>
                    ) : (
                      <>
                        <MessageSquare className="w-4 h-4 mr-2" />
                        Summarize
                      </>
                    )}
                  </Button>
                  {summaryText && (
                    <div
                      className={`p-4 rounded-lg ${
                        theme === "dark" ? "bg-gray-800 border-gray-700" : "bg-gray-50 border-gray-200"
                      } border`}
                    >
                      <p className="text-sm">{summaryText}</p>
                    </div>
                  )}
                </motion.div>
              )}

              {activeTab === "explain" && (
                <motion.div
                  className="space-y-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div>
                    <label className="block text-sm font-medium mb-2">Complex Topic</label>
                    <Textarea
                      placeholder="Enter a complex topic you want explained simply..."
                      className={`${
                        theme === "dark"
                          ? "bg-gray-800 border-gray-700 text-white"
                          : "bg-gray-50 border-gray-300 text-gray-900"
                      }`}
                      rows={4}
                    />
                  </div>
                  <Button
                    onClick={handleExplain}
                    disabled={isGenerating}
                    className={`w-full ${
                      theme === "dark"
                        ? "bg-gradient-to-r from-[#FF00FF] to-[#00FFFF] text-black"
                        : "bg-gradient-to-r from-purple-600 to-indigo-600 text-white"
                    }`}
                  >
                    {isGenerating ? (
                      <>
                        <Zap className="w-4 h-4 mr-2 animate-spin" />
                        Explaining...
                      </>
                    ) : (
                      <>
                        <Lightbulb className="w-4 h-4 mr-2" />
                        Explain Simply
                      </>
                    )}
                  </Button>
                  {explainText && (
                    <div
                      className={`p-4 rounded-lg ${
                        theme === "dark" ? "bg-gray-800 border-gray-700" : "bg-gray-50 border-gray-200"
                      } border`}
                    >
                      <p className="text-sm">{explainText}</p>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
