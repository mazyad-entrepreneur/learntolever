import { useEffect, useState } from "react";
import { getSeriesList } from "../api/client";
import SeriesCard from "../components/SeriesCard";

/**
 * Homepage — shows learning series (Level 1).
 */
export default function HomePage() {
  const [seriesList, setSeriesList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSeriesList()
      .then((data) => setSeriesList(data.results || data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-3 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {/* Hero section */}
      <header className="text-center py-8 md:py-14">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 text-sm font-medium mb-4">
          <span className="w-2 h-2 rounded-full bg-brand-500 animate-pulse" />
          Interactive Learning Platform
        </div>
        <h1 className="text-gray-900 dark:text-white mb-4">
          Learn Programming,{" "}
          <span className="bg-gradient-to-r from-brand-500 to-brand-700 bg-clip-text text-transparent">
            Step by Step
          </span>
        </h1>
        <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
          Master the fundamentals of programming through structured lessons,
          hands-on code examples, and guided problem-solving.
        </p>
      </header>

      {/* Series grid */}
      <section>
        <h2 className="text-gray-900 dark:text-white mb-6">
          📚 Learning Paths
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
          {seriesList.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400">No learning series published yet.</p>
          ) : (
            seriesList.map((series) => (
              <SeriesCard key={series.slug} series={series} />
            ))
          )}
        </div>
      </section>

      {/* Platform features */}
      <section className="content-section">
        <h2 className="text-gray-900 dark:text-white mb-6">
          ✨ How This Platform Works
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[
            { icon: "📖", title: "Read", desc: "Clear explanations with code examples for every concept." },
            { icon: "🧠", title: "Understand", desc: "Logic breakdowns and visual explanations build intuition." },
            { icon: "💪", title: "Practice", desc: "Guided problems and assignments reinforce your learning." },
          ].map(({ icon, title, desc }) => (
            <div key={title} className="text-center">
              <div className="text-3xl mb-2">{icon}</div>
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-1">{title}</h4>
              <p className="text-sm text-gray-500 dark:text-gray-400">{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
