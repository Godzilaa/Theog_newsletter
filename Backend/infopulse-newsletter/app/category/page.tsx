

import Link from 'next/link';
import { healthCheck } from '@/lib/api';

export default async function CategoryListPage() {
  let categories: string[] = [];
  try {
    const health = await healthCheck();
    // If backend exposes categories in health, use it; otherwise, use static fallback
    categories = health?.services?.categories || [
      'general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'
    ];
  } catch {
    categories = [
      'general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'
    ];
  }

  return (
    <div className="max-w-xl mx-auto py-12">
      <h1 className="text-2xl font-bold mb-6">News Categories</h1>
      <ul className="space-y-4">
        {categories.map((cat) => (
          <li key={cat}>
            <Link href={`/category/${cat}`} className="text-blue-600 hover:underline capitalize text-lg">
              {cat}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

