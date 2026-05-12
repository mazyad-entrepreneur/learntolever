import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getModule } from "../api/client";
import TopicList from "../components/TopicList";

/**
 * Module detail page — shows module info and topic list.
 */
export default function ModulePage() {
  const { slug } = useParams();
  const [module, setModule] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getModule(slug)
      .then(setModule)
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

  if (!module) {
    return <p className="text-center text-gray-400 py-20">Module not found.</p>;
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-400 dark:text-gray-500">
        <Link to="/" className="hover:text-brand-500 no-underline">Home</Link>
        <span>/</span>
        <span className="text-gray-700 dark:text-gray-300">{module.title}</span>
      </nav>

      {/* Module header */}
      <header className="content-section">
        <div className="flex items-center gap-4 mb-3">
          <span className="text-4xl">{module.icon}</span>
          <div>
            <h1 className="text-gray-900 dark:text-white">{module.title}</h1>
            <p className="text-sm text-gray-400 mt-1">
              {module.topics?.length || 0} topics
            </p>
          </div>
        </div>
        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
          {module.description}
        </p>

        {/* Quick links */}
        <div className="flex gap-3 mt-4">
          <Link
            to={`/module/${slug}/revision`}
            className="px-4 py-2 text-sm rounded-lg bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 hover:bg-brand-100 dark:hover:bg-brand-900/50 no-underline transition-colors"
          >
            📝 Revision Notes
          </Link>
        </div>
      </header>

      {/* Topics */}
      <section>
        <h2 className="text-gray-900 dark:text-white mb-4">📋 Topics</h2>
        <TopicList topics={module.topics} moduleSlug={slug} />
      </section>
    </div>
  );
}
