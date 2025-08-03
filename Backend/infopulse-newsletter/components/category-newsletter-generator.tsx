'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Newspaper } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { fetchCategoryArticles, type NewsArticle } from '@/lib/api';

const CATEGORIES = [
  'technology',
  'business',
  'science',
  'health',
  'sports',
  'entertainment',
  'general'
];

export default function CategoryArticleViewer() {
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState<NewsArticle[]>([]);

  const handleCategoryArticles = async () => {
    if (!selectedCategory) {
      toast({
        title: "Error",
        description: "Please select a category first",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const categoryArticles = await fetchCategoryArticles(selectedCategory);
      setArticles(categoryArticles);
      toast({
        title: "Success",
        description: `Found ${categoryArticles.length} articles in ${selectedCategory}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch articles",
        variant: "destructive",
      });
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">📰 Category Article Viewer</h1>
        <p className="text-gray-600">Browse and fetch news articles by category</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Newspaper className="w-5 h-5" />
            Category Articles
          </CardTitle>
          <CardDescription>
            Select a category and fetch the latest articles
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">Select Category:</label>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a news category" />
              </SelectTrigger>
              <SelectContent>
                {CATEGORIES.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button
            onClick={handleCategoryArticles}
            disabled={loading || !selectedCategory}
            variant="outline"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
            Fetch Articles
          </Button>
        </CardContent>
      </Card>

      {articles.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>📰 Fetched Articles ({articles.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {articles.map((article, index) => (
                <Card key={index} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <h4 className="font-medium text-sm mb-2 line-clamp-2">{article.title}</h4>
                    {article.description && (
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                        {article.description}
                      </p>
                    )}
                    <div className="flex justify-between items-center text-xs text-gray-500">
                      <span className="font-medium">{article.source}</span>
                      <time dateTime={article.published_at}>
                        {new Date(article.published_at).toLocaleDateString()}
                      </time>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
