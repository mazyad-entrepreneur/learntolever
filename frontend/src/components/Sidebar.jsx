import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { getModules, getModule } from "../api/client";
import { SidebarAd } from "./ads/SidebarAd";

/**
 * Sidebar navigation — shows all modules and their topics.
 * Collapses on mobile (overlay), always visible on desktop.
 */
export default function Sidebar({ isOpen, onClose }) {
  const [modules, setModules] = useState([]);
  const [expanded, setExpanded] = useState(null);
  const [topics, setTopics] = useState({});

  useEffect(() => {
    getModules()
      .then((data) => setModules(data.results || data))
      .catch(console.error);
  }, []);

  const toggleModule = async (slug) => {
    if (expanded === slug) {
      setExpanded(null);
      return;
    }
    setExpanded(slug);
    // Fetch topics for this module if not already cached
    if (!topics[slug]) {
      try {
        const mod = await getModule(slug);
        setTopics((prev) => ({ ...prev, [slug]: mod.topics || [] }));
      } catch (err) {
        console.error("Failed to load topics:", err);
      }
    }
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:sticky top-16 left-0 z-40
          w-72 h-[calc(100vh-4rem)] overflow-y-auto
          bg-white dark:bg-surface-800
          border-r border-gray-200 dark:border-gray-700/50
          custom-scrollbar
          transition-transform duration-300
          ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
          lg:block
        `}
      >
        <div className="p-4">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-3 px-2">
            Modules
          </h3>

          <nav className="space-y-1">
            {modules.map((mod) => (
              <div key={mod.slug}>
                {/* Module header */}
                <button
                  onClick={() => toggleModule(mod.slug)}
                  className="w-full flex items-center gap-2 px-3 py-2.5 rounded-lg text-left text-sm font-medium
                    text-gray-700 dark:text-gray-200
                    hover:bg-brand-50 dark:hover:bg-surface-700 transition-colors"
                >
                  <span className="text-lg">{mod.icon}</span>
                  <span className="flex-1 truncate">{mod.title}</span>
                  <svg
                    className={`w-4 h-4 text-gray-400 transition-transform ${
                      expanded === mod.slug ? "rotate-90" : ""
                    }`}
                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>

                {/* Topic list (expandable) */}
                {expanded === mod.slug && (
                  <div className="ml-4 pl-4 border-l-2 border-brand-200 dark:border-brand-800 space-y-0.5 mt-1 mb-2">
                    <Link
                      to={`/module/${mod.slug}`}
                      onClick={onClose}
                      className="block px-3 py-1.5 text-sm rounded-md text-brand-600 dark:text-brand-400 hover:bg-brand-50 dark:hover:bg-surface-700 no-underline font-medium"
                    >
                      📋 Overview
                    </Link>
                    {/* Individual topics */}
                    {(topics[mod.slug] || []).map((topic) => (
                      <Link
                        key={topic.slug}
                        to={`/topic/${topic.slug}`}
                        onClick={onClose}
                        className="block px-3 py-1.5 text-sm rounded-md text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-surface-700 hover:text-brand-600 dark:hover:text-brand-400 no-underline transition-colors"
                      >
                        {topic.title}
                      </Link>
                    ))}
                    <Link
                      to={`/module/${mod.slug}/revision`}
                      onClick={onClose}
                      className="block px-3 py-1.5 text-sm rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-surface-700 no-underline"
                    >
                      📝 Revision Notes
                    </Link>
                  </div>
                )}
              </div>
            ))}
          </nav>

          {/* Sidebar ad slot */}
          <SidebarAd />
        </div>
      </aside>
    </>
  );
}
