import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getSeries } from "../api/client";
import ModuleCard from "../components/ModuleCard";

export default function SeriesPage() {
  const { slug } = useParams();
  const [series, setSeries] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSeries(slug)
      .then(setSeries)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-3 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!series) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Series Not Found</h2>
        <p className="text-gray-500 dark:text-gray-400 mb-6">The series you're looking for doesn't exist or isn't published yet.</p>
        <Link to="/" className="text-brand-600 hover:underline">← Back to Home</Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      <Link to="/" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors no-underline">
        ← Back to Home
      </Link>

      <header className="content-section">
        <div className="flex items-start gap-4 md:gap-6">
          <div className="w-16 h-16 md:w-20 md:h-20 rounded-2xl bg-brand-50 dark:bg-brand-900/20 flex items-center justify-center text-4xl md:text-5xl flex-shrink-0">
            {series.icon}
          </div>
          <div>
            <h1 className="mb-2 text-2xl md:text-3xl text-gray-900 dark:text-white">{series.title}</h1>
            <p className="text-gray-500 dark:text-gray-400 text-sm md:text-base leading-relaxed max-w-3xl">
              {series.description}
            </p>
          </div>
        </div>
      </header>

      <section>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          <span>📚</span> Modules in this Series
        </h2>
        
        {series.modules?.length === 0 ? (
          <div className="content-section text-center py-12 text-gray-500 dark:text-gray-400">
            No modules published in this series yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
            {series.modules?.map((mod) => (
              <ModuleCard key={mod.slug} module={mod} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
