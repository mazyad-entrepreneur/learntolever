import { useState, useEffect } from "react";
import { Link, Outlet, useNavigate, useLocation } from "react-router-dom";
import { isLoggedIn, logout, getMe, fetchSeries } from "../api/studioApi";

export default function StudioLayout() {
  const [user, setUser] = useState(null);
  const [series, setSeries] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const nav = useNavigate();
  const loc = useLocation();

  useEffect(() => {
    if (!isLoggedIn()) { nav("/studio/login"); return; }
    getMe().then(setUser).catch(() => nav("/studio/login"));
    loadSeries();
  }, []);

  const loadSeries = async () => {
    try {
      const data = await fetchSeries();
      setSeries(data.results || data || []);
    } catch { /* ignore */ }
  };

  const handleLogout = () => { logout(); nav("/studio/login"); };

  const isActive = (path) => loc.pathname === path || loc.pathname.startsWith(path + "/");

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-surface-900 flex">
      {/* Sidebar */}
      <aside
        className={`${sidebarOpen ? "w-64" : "w-0 overflow-hidden"} transition-all duration-200 bg-white dark:bg-surface-800 border-r border-gray-200 dark:border-gray-700/30 flex flex-col flex-shrink-0`}
      >
        {/* Header */}
        <div className="p-4 border-b border-gray-100 dark:border-gray-700/30">
          <Link to="/studio" className="flex items-center gap-2 no-underline">
            <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
              L
            </div>
            <span className="font-bold text-gray-900 dark:text-white text-sm">
              Creator Studio
            </span>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          <NavItem to="/studio" label="📊 Dashboard" active={loc.pathname === "/studio"} />
          <NavItem to="/studio/series/new" label="＋ New Series" active={isActive("/studio/series/new")} accent />

          {/* Series tree */}
          <div className="mt-4 mb-2 px-2 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
            Series
          </div>
          {(Array.isArray(series) ? series : []).map((s) => (
            <NavItem
              key={s.id}
              to={`/studio/series/${s.id}`}
              label={`${s.icon || "📘"} ${s.title}`}
              active={isActive(`/studio/series/${s.id}`)}
            />
          ))}

          <div className="mt-6 mb-2 px-2 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
            Quick Access
          </div>
          <NavItem to="/studio/drafts" label="📝 Drafts" active={isActive("/studio/drafts")} />
        </nav>

        {/* User */}
        <div className="p-3 border-t border-gray-100 dark:border-gray-700/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 min-w-0">
              <div className="w-7 h-7 bg-brand-100 dark:bg-brand-900/30 rounded-lg flex items-center justify-center text-brand-600 dark:text-brand-400 text-xs font-bold flex-shrink-0">
                {user?.username?.[0]?.toUpperCase() || "?"}
              </div>
              <span className="text-sm text-gray-700 dark:text-gray-300 truncate">
                {user?.username || "..."}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="text-xs text-gray-400 hover:text-rose-500 transition-colors"
              title="Sign out"
            >
              ↗
            </button>
          </div>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-12 bg-white dark:bg-surface-800 border-b border-gray-200 dark:border-gray-700/30 flex items-center px-4 gap-3 flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
          >
            {sidebarOpen ? "◀" : "▶"}
          </button>
          <span className="text-sm text-gray-400">
            {loc.pathname.replace("/studio", "").replace(/\//g, " › ").trim() || "Dashboard"}
          </span>
          <div className="flex-1" />
          <a
            href="/"
            target="_blank"
            rel="noopener"
            className="text-xs text-gray-400 hover:text-brand-500 no-underline"
          >
            View site →
          </a>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet context={{ loadSeries }} />
        </main>
      </div>
    </div>
  );
}

function NavItem({ to, label, active, accent }) {
  return (
    <Link
      to={to}
      className={`block px-3 py-2 rounded-lg text-sm no-underline transition-all ${
        active
          ? "bg-brand-50 dark:bg-brand-900/20 text-brand-700 dark:text-brand-300 font-medium"
          : accent
          ? "text-brand-600 dark:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/10"
          : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-surface-700"
      }`}
    >
      {label}
    </Link>
  );
}
