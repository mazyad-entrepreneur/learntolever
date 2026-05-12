import { Link } from "react-router-dom";

/**
 * Card component for displaying a module on the homepage.
 */
export default function ModuleCard({ module }) {
  return (
    <Link
      to={`/module/${module.slug}`}
      className="group block no-underline hover:no-underline"
    >
      <div className="content-section h-full flex flex-col gap-3 group-hover:border-brand-300 dark:group-hover:border-brand-700 group-hover:-translate-y-1 transition-all duration-300">
        {/* Icon + Title */}
        <div className="flex items-center gap-3">
          <span className="text-3xl">{module.icon}</span>
          <div>
            <h3 className="text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">
              {module.title}
            </h3>
            <span className="text-xs text-gray-400">
              {module.topic_count} topic{module.topic_count !== 1 ? "s" : ""}
            </span>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed flex-1">
          {module.description}
        </p>

        {/* CTA */}
        <div className="flex items-center gap-1 text-sm font-medium text-brand-600 dark:text-brand-400">
          Start Learning
          <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
    </Link>
  );
}
