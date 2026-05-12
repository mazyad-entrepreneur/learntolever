import { Link } from "react-router-dom";

export default function SeriesCard({ series }) {
  return (
    <Link
      to={`/series/${series.slug}`}
      className="block group bg-white dark:bg-surface-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700/30 transition-all duration-300 hover:shadow-md dark:hover:shadow-lg dark:hover:bg-surface-800/80 no-underline"
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-brand-50 dark:bg-brand-900/20 text-2xl group-hover:scale-110 transition-transform duration-300">
          {series.icon || "📚"}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-xs font-semibold tracking-wider text-gray-400 dark:text-gray-500 uppercase">
              {series.module_count} {series.module_count === 1 ? "module" : "modules"}
            </span>
            <span className="text-brand-600 dark:text-brand-400 opacity-0 group-hover:opacity-100 transition-opacity translate-x-2 group-hover:translate-x-0 duration-300">
              →
            </span>
          </div>

          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 leading-tight group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">
            {series.title}
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed line-clamp-2">
            {series.description}
          </p>
        </div>
      </div>
    </Link>
  );
}
