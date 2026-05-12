import { useState, useEffect } from "react";
import { Link, useOutletContext } from "react-router-dom";
import {
  fetchSeries, createSeries, deleteSeries,
} from "../api/studioApi";

export default function StudioDashboard() {
  const [series, setSeries] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newIcon, setNewIcon] = useState("📘");
  const { loadSeries: refreshSidebar } = useOutletContext();

  useEffect(() => { load(); }, []);

  const load = async () => {
    const data = await fetchSeries();
    setSeries(data.results || data || []);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    await createSeries({ title: newTitle, description: newDesc, icon: newIcon, is_published: false });
    setNewTitle(""); setNewDesc(""); setShowNew(false);
    load(); refreshSidebar();
  };

  const handleDelete = async (id, title) => {
    if (!confirm(`Delete "${title}" and all its modules/topics?`)) return;
    await deleteSeries(id);
    load(); refreshSidebar();
  };

  return (
    <div className="max-w-4xl mx-auto fade-in">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Creator Dashboard
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Manage your learning series, modules, and topics
          </p>
        </div>
        <button
          onClick={() => setShowNew(!showNew)}
          className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-xl transition-all"
        >
          + New Series
        </button>
      </div>

      {/* New Series Form */}
      {showNew && (
        <form onSubmit={handleCreate} className="content-section mb-6 space-y-3">
          <h3 className="font-semibold text-gray-900 dark:text-white">Create New Series</h3>
          <div className="flex gap-3">
            <input
              value={newIcon} onChange={(e) => setNewIcon(e.target.value)}
              className="w-16 px-3 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-center text-lg"
              placeholder="📘"
            />
            <input
              value={newTitle} onChange={(e) => setNewTitle(e.target.value)}
              className="flex-1 px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white"
              placeholder="Series title..."
              required autoFocus
            />
          </div>
          <textarea
            value={newDesc} onChange={(e) => setNewDesc(e.target.value)}
            className="w-full px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white text-sm"
            placeholder="Brief description..."
            rows={2}
          />
          <div className="flex gap-2">
            <button type="submit" className="px-4 py-2 bg-brand-600 text-white text-sm rounded-xl hover:bg-brand-700">
              Create
            </button>
            <button type="button" onClick={() => setShowNew(false)} className="px-4 py-2 text-gray-500 text-sm">
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Series Cards */}
      <div className="space-y-3">
        {series.length === 0 && !showNew && (
          <div className="content-section text-center py-12 text-gray-400">
            <p className="text-4xl mb-3">📚</p>
            <p>No series yet. Create your first learning series to get started.</p>
          </div>
        )}
        {series.map((s) => (
          <Link
            key={s.id}
            to={`/studio/series/${s.id}`}
            className="content-section flex items-center gap-4 no-underline group"
          >
            <span className="text-3xl">{s.icon || "📘"}</span>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-gray-900 dark:text-white group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">
                {s.title}
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 truncate">{s.description}</p>
              <div className="flex gap-3 mt-1 text-xs text-gray-400">
                <span>{s.module_count || 0} modules</span>
                <span className={s.is_published ? "text-emerald-500" : "text-amber-500"}>
                  {s.is_published ? "● Published" : "● Draft"}
                </span>
              </div>
            </div>
            <span className="text-gray-300 dark:text-gray-600 group-hover:text-brand-400 transition-colors">
              →
            </span>
            <button
              onClick={(e) => { e.preventDefault(); e.stopPropagation(); handleDelete(s.id, s.title); }}
              className="text-gray-300 hover:text-rose-500 transition-colors text-sm opacity-0 group-hover:opacity-100"
              title="Delete series"
            >
              ✕
            </button>
          </Link>
        ))}
      </div>
    </div>
  );
}
