
import { fetchCategoryArticles, NewsArticle } from '@/lib/api';
import { notFound } from 'next/navigation';

export const dynamic = 'force-dynamic'; // Enable SSR for dynamic params

export default async function CategoryPage({ params }: { params: { category: string } }) {
  const { category } = params;
  let articles: NewsArticle[] = [];
  let error = '';

  try {
    articles = await fetchCategoryArticles(category, 10);
  } catch (e: any) {
    error = e?.message || 'Failed to fetch articles.';
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto py-12">
        <h1 className="text-2xl font-bold mb-4 capitalize">{category} News</h1>
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!articles.length) {
    return notFound();
  }

  return (
    <div className="max-w-2xl mx-auto py-12">
      <h1 className="text-2xl font-bold mb-4 capitalize">{category} News</h1>
      <div className="space-y-6">
        {articles.map((article, idx) => (
          <div key={idx} className="border rounded-lg p-4 bg-white shadow">
            <h2 className="font-semibold text-lg mb-2">{article.title}</h2>
            <p className="text-gray-700 mb-2">{article.description}</p>
            {article.image_url && (
              <img src={article.image_url} alt={article.title} className="w-full max-w-md rounded mb-2" />
            )}
            <div className="text-xs text-gray-500 flex justify-between">
              <span>{article.source}</span>
              <span>{new Date(article.published_at).toLocaleDateString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
