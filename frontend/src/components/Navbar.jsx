import { Link } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

/**
 * Top navigation bar with logo, search placeholder, and theme toggle.
 */
export default function Navbar({ darkMode, setDarkMode, onMenuToggle }) {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-surface-800/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-700/50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Left: menu + logo */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuToggle}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-surface-700 transition-colors"
            aria-label="Toggle menu"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <Link to="/" className="flex items-center gap-2 no-underline hover:no-underline">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white font-bold text-sm shadow-md">
              L
            </div>
            <span className="text-lg font-bold text-gray-900 dark:text-white hidden sm:block">
              LearnToLever
            </span>
          </Link>
        </div>

        {/* Right: theme toggle */}
        <div className="flex items-center gap-3">
          <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
        </div>
      </div>
    </nav>
  );
}
