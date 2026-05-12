import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { useState, useEffect } from "react";
// Public
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import SeriesPage from "./pages/SeriesPage";
import ModulePage from "./pages/ModulePage";
import TopicPage from "./pages/TopicPage";
import RevisionPage from "./pages/RevisionPage";

// Studio
import StudioLayout from "./studio/StudioLayout";
import StudioLogin from "./studio/StudioLogin";
import StudioDashboard from "./studio/StudioDashboard";
import SeriesEditor from "./studio/SeriesEditor";
import TopicEditor from "./studio/TopicEditor";

function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-50 dark:bg-surface-900">
      <div className="text-center">
        <p className="text-6xl mb-4">🔍</p>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Page Not Found</h1>
        <p className="text-gray-500 dark:text-gray-400 mb-6">The page you're looking for doesn't exist.</p>
        <Link to="/" className="px-6 py-3 bg-brand-600 text-white rounded-xl hover:bg-brand-700 no-underline transition-all">
          ← Back to Home
        </Link>
      </div>
    </div>
  );
}

export default function App() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
    }
    return false;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  return (
    <BrowserRouter>
      <Routes>
        {/* Studio Auth */}
        <Route path="/studio/login" element={<StudioLogin />} />

        {/* Studio App */}
        <Route path="/studio" element={<StudioLayout />}>
          <Route index element={<StudioDashboard />} />
          <Route path="series/:id" element={<SeriesEditor />} />
          <Route path="topic/:id" element={<TopicEditor />} />
        </Route>

        {/* Public App (wrapped in public Layout) */}
        <Route element={<Layout darkMode={darkMode} setDarkMode={setDarkMode} />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/series/:slug" element={<SeriesPage />} />
          <Route path="/module/:slug" element={<ModulePage />} />
          <Route path="/topic/:slug" element={<TopicPage />} />
          <Route path="/module/:slug/revision" element={<RevisionPage />} />
        </Route>

        {/* 404 Catch-all */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
