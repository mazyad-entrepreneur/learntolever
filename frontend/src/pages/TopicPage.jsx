import { useEffect, useState } from "react";
import { useParams, Link, useLocation } from "react-router-dom";
import { getTopic } from "../api/client";
import ContentRenderer from "../components/ContentRenderer";
import ProblemCard from "../components/ProblemCard";
import LivePreview from "../studio/components/LivePreview";
import { InlineAd } from "../components/ads/InlineAd";

/**
 * Topic detail page — full lesson content + problems.
 */
export default function TopicPage() {
  const { slug } = useParams();
  const location = useLocation();
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getTopic(slug)
      .then(setTopic)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [slug]);

  useEffect(() => {
    if (topic && location.hash) {
      setTimeout(() => {
        const id = location.hash.replace("#", "");
        const element = document.getElementById(id);
        if (element) {
          element.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 100);
    }
  }, [topic, location.hash]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-3 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!topic) {
    return <p className="text-center text-gray-400 py-20">Topic not found.</p>;
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-400 dark:text-gray-500 flex-wrap">
        <Link to="/" className="hover:text-brand-500 no-underline">Home</Link>
        <span>/</span>
        <Link to={`/module/${topic.module_slug}`} className="hover:text-brand-500 no-underline">
          {topic.module_title}
        </Link>
        <span>/</span>
        <span className="text-gray-700 dark:text-gray-300">{topic.title}</span>
      </nav>

      {/* Topic title */}
      <header>
        <h1 className="text-gray-900 dark:text-white">{topic.title}</h1>
        <p className="text-sm text-gray-400 mt-1">
          Last updated: {new Date(topic.updated_at).toLocaleDateString()}
        </p>
      </header>

      {/* Content sections: Render Blocks if available, else Legacy ContentRenderer */}
      {topic.blocks && topic.blocks.length > 0 ? (
        <div className="bg-white dark:bg-surface-800 rounded-2xl p-6 md:p-8 shadow-sm border border-gray-100 dark:border-gray-700/30">
          <LivePreview blocks={topic.blocks} />
        </div>
      ) : (
        <ContentRenderer topic={topic} />
      )}

      {/* Inline ad slot between content and problems */}
      <InlineAd />

      {/* Problems section */}
      {topic.problems && topic.problems.length > 0 && (
        <section>
          <h2 className="text-gray-900 dark:text-white mb-4">
            🏋️ Practice Problems
          </h2>
          <div className="space-y-4">
            {topic.problems.map((problem) => (
              <ProblemCard key={problem.id} problem={problem} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
