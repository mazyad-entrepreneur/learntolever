import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getModuleRevision } from "../api/client";
import RevisionNotes from "../components/RevisionNotes";

/**
 * Revision page — quick reference notes for a module.
 */
export default function RevisionPage() {
  const { slug } = useParams();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getModuleRevision(slug)
      .then((data) => setNotes(data.results || data))
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

  return (
    <div className="space-y-8 fade-in">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-400 dark:text-gray-500">
        <Link to="/" className="hover:text-brand-500 no-underline">Home</Link>
        <span>/</span>
        <Link to={`/module/${slug}`} className="hover:text-brand-500 no-underline">{slug}</Link>
        <span>/</span>
        <span className="text-gray-700 dark:text-gray-300">Revision</span>
      </nav>

      <header>
        <h1 className="text-gray-900 dark:text-white">📝 Revision Notes</h1>
        <p className="text-sm text-gray-400 mt-1">
          Quick reference and key takeaways
        </p>
      </header>

      <RevisionNotes notes={notes} />
    </div>
  );
}
