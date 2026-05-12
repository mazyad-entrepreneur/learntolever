import { Link } from "react-router-dom";

/**
 * Displays a list of topics for a module.
 */
export default function TopicList({ topics, moduleSlug }) {
  if (!topics || topics.length === 0) {
    return (
      <p className="text-gray-400 dark:text-gray-500 text-sm italic">
        No topics published yet.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {topics.map((topic, idx) => (
        <Link
          key={topic.slug}
          to={`/topic/${topic.slug}`}
          className="group flex items-center gap-4 p-4 rounded-xl
            bg-white dark:bg-surface-800
            border border-gray-100 dark:border-gray-700/30
            hover:border-brand-300 dark:hover:border-brand-700
            hover:shadow-md transition-all duration-200 no-underline"
        >
          {/* Number badge */}
          <div className="w-8 h-8 rounded-lg bg-brand-50 dark:bg-brand-900/30 flex items-center justify-center text-sm font-bold text-brand-600 dark:text-brand-400 flex-shrink-0">
            {idx + 1}
          </div>

          {/* Topic info */}
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-medium text-gray-800 dark:text-gray-200 group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors truncate">
              {topic.title}
            </h4>
          </div>

          {/* Arrow */}
          <svg
            className="w-4 h-4 text-gray-300 dark:text-gray-600 group-hover:text-brand-500 group-hover:translate-x-0.5 transition-all flex-shrink-0"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      ))}
    </div>
  );
}
