import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { searchTopics } from "../api/client";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await searchTopics(query);
        setResults(data);
        setIsOpen(true);
      } catch (err) {
        console.error("Search failed", err);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  const handleResultClick = (topic_slug, section_id) => {
    setIsOpen(false);
    setQuery("");
    const hash = section_id ? `#${section_id}` : "";
    navigate(`/topic/${topic_slug}${hash}`);
  };

  return (
    <div ref={wrapperRef} className="relative w-full max-w-md flex-1 mx-4 lg:mx-8">
      <div className="relative flex items-center">
        <svg
          className="absolute left-3 w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => { if (query.trim()) setIsOpen(true); }}
          placeholder="Search topics..."
          className="w-full pl-10 pr-10 py-2 bg-gray-100 dark:bg-surface-700/50 border border-transparent dark:border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-brand-500 transition-all text-sm text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
        />
        {loading && (
          <div className="absolute right-3 w-4 h-4 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
        )}
      </div>

      {isOpen && (query.trim() !== "") && (
        <div className="absolute top-full mt-2 w-full bg-white dark:bg-surface-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-xl overflow-hidden z-50">
          <div className="max-h-96 overflow-y-auto">
            {results.length === 0 && !loading ? (
              <div className="p-4 text-center text-sm text-gray-500 dark:text-gray-400">
                No results found.
              </div>
            ) : (
              results.map((res, idx) => {
                // Escape HTML for safety, but allow highlighting
                const safeSnippet = res.snippet
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;");
                
                // Highlight the query
                const regex = new RegExp(`(${query})`, "gi");
                const highlighted = safeSnippet.replace(regex, '<strong class="text-brand-500 dark:text-brand-400">$1</strong>');

                return (
                  <button
                    key={idx}
                    onClick={() => handleResultClick(res.topic_slug, res.section_id)}
                    className="w-full text-left p-4 hover:bg-gray-50 dark:hover:bg-surface-700/50 border-b border-gray-100 dark:border-gray-700/50 last:border-0 transition-colors"
                  >
                    <div className="text-sm font-semibold text-gray-900 dark:text-white">
                      {res.topic_title}
                    </div>
                    <div 
                      className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-2" 
                      dangerouslySetInnerHTML={{ __html: highlighted }} 
                    />
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}
