"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'

// Renamed from NewsletterGenerator to CategoryNavbar
export function CategoryNavbar() {
  const pathname = usePathname()

  const categories = [
    { id: 'technology', label: 'Technology' },
    { id: 'business', label: 'Business' },
    { id: 'science', label: 'Science' },
    { id: 'health', label: 'Health' },
    { id: 'sports', label: 'Sports' },
    { id: 'entertainment', label: 'Entertainment' },
    { id: 'general', label: 'General' }
  ]

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-center space-x-8 py-4">
          {categories.map((category) => {
            const isActive = pathname.includes(`/category/${category.id}`)
            return (
              <Link
                key={category.id}
                href={`/category/${category.id}`}
                className={`text-sm font-medium transition-colors hover:text-blue-600 ${
                  isActive 
                    ? 'text-blue-600' 
                    : 'text-gray-600 dark:text-gray-300'
                }`}
              >
                {category.label}
              </Link>
            )
          })}
        </div>
      </div>
    </nav>
  )
}
