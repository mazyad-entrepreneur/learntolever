import { useState, useEffect } from "react";
import { useParams, Link, useOutletContext } from "react-router-dom";
import {
  fetchSeries, updateSeries,
  fetchModules, createModule, updateModule, deleteModule,
  fetchTopics,
} from "../api/studioApi";

export default function SeriesEditor() {
  const { id } = useParams();
  const [series, setSeries] = useState(null);
  const [modules, setModules] = useState([]);
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [icon, setIcon] = useState("");
  const [showNewModule, setShowNewModule] = useState(false);
  const [newModTitle, setNewModTitle] = useState("");
  const [newModDesc, setNewModDesc] = useState("");
  const [newModIcon, setNewModIcon] = useState("📘");
  const [expandedMod, setExpandedMod] = useState(null);
  const [topics, setTopics] = useState({});
  const { loadSeries: refreshSidebar } = useOutletContext();

  useEffect(() => { load(); }, [id]);

  const load = async () => {
    const data = await fetchSeries();
    const all = data.results || data || [];
    const s = all.find((x) => x.id === parseInt(id));
    if (s) { setSeries(s); setTitle(s.title); setDesc(s.description); setIcon(s.icon); }
    const mods = await fetchModules(id);
    setModules(mods.results || mods || []);
  };

  const handleSaveSeries = async () => {
    await updateSeries(id, { title, description: desc, icon });
    setEditing(false); load(); refreshSidebar();
  };

  const handlePublishToggle = async () => {
    await updateSeries(id, { is_published: !series.is_published });
    load(); refreshSidebar();
  };

  const handleCreateModule = async (e) => {
    e.preventDefault();
    await createModule({ series: parseInt(id), title: newModTitle, description: newModDesc, icon: newModIcon });
    setNewModTitle(""); setNewModDesc(""); setShowNewModule(false);
    load();
  };

  const handleDeleteModule = async (modId, modTitle) => {
    if (!confirm(`Delete "${modTitle}" and all its topics?`)) return;
    await deleteModule(modId);
    load();
  };

  const handleToggleModPublish = async (mod) => {
    await updateModule(mod.id, { is_published: !mod.is_published });
    load();
  };

  const loadTopics = async (modId) => {
    if (expandedMod === modId) { setExpandedMod(null); return; }
    const data = await fetchTopics(modId);
    setTopics((prev) => ({ ...prev, [modId]: data.results || data || [] }));
    setExpandedMod(modId);
  };

  if (!series) return <div className="text-gray-400">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto fade-in">
      {/* Series Header */}
      <div className="content-section mb-6">
        {editing ? (
          <div className="space-y-3">
            <div className="flex gap-3">
              <input value={icon} onChange={(e) => setIcon(e.target.value)}
                className="w-16 px-3 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-center text-lg" />
              <input value={title} onChange={(e) => setTitle(e.target.value)}
                className="flex-1 px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white font-bold text-xl" />
            </div>
            <textarea value={desc} onChange={(e) => setDesc(e.target.value)}
              className="w-full px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white text-sm" rows={2} />
            <div className="flex gap-2">
              <button onClick={handleSaveSeries} className="px-4 py-2 bg-brand-600 text-white text-sm rounded-xl hover:bg-brand-700">Save</button>
              <button onClick={() => setEditing(false)} className="px-4 py-2 text-gray-500 text-sm">Cancel</button>
            </div>
          </div>
        ) : (
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <span className="text-3xl">{series.icon}</span> {series.title}
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{series.description}</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setEditing(true)}
                className="px-3 py-1.5 text-sm text-gray-500 hover:text-brand-600 border border-gray-200 dark:border-gray-600 rounded-lg">
                Edit
              </button>
              <button onClick={handlePublishToggle}
                className={`px-3 py-1.5 text-sm rounded-lg font-medium ${
                  series.is_published
                    ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
                    : "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
                }`}>
                {series.is_published ? "● Published" : "● Draft"}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modules Section */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">📦 Modules</h2>
        <button onClick={() => setShowNewModule(!showNewModule)}
          className="px-3 py-1.5 bg-brand-600 hover:bg-brand-700 text-white text-sm rounded-lg">
          + Add Module
        </button>
      </div>

      {showNewModule && (
        <form onSubmit={handleCreateModule} className="content-section mb-4 space-y-3">
          <div className="flex gap-3">
            <input value={newModIcon} onChange={(e) => setNewModIcon(e.target.value)}
              className="w-14 px-2 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-center" />
            <input value={newModTitle} onChange={(e) => setNewModTitle(e.target.value)}
              className="flex-1 px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-900 dark:text-white"
              placeholder="Module title..." required autoFocus />
          </div>
          <textarea value={newModDesc} onChange={(e) => setNewModDesc(e.target.value)}
            className="w-full px-4 py-2 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-xl text-sm text-gray-900 dark:text-white"
            placeholder="Description..." rows={2} />
          <div className="flex gap-2">
            <button type="submit" className="px-4 py-2 bg-brand-600 text-white text-sm rounded-xl">Create</button>
            <button type="button" onClick={() => setShowNewModule(false)} className="px-4 py-2 text-gray-500 text-sm">Cancel</button>
          </div>
        </form>
      )}

      {/* Module List */}
      <div className="space-y-2">
        {modules.length === 0 && (
          <div className="content-section text-center py-8 text-gray-400">No modules yet.</div>
        )}
        {modules.map((mod) => (
          <div key={mod.id} className="content-section">
            <div className="flex items-center gap-3 cursor-pointer" onClick={() => loadTopics(mod.id)}>
              <span className="text-xl">{mod.icon}</span>
              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-gray-900 dark:text-white">{mod.title}</h3>
                <p className="text-xs text-gray-400 truncate">{mod.description}</p>
              </div>
              <span className="text-xs text-gray-400">{mod.topic_count || 0} topics</span>
              <button onClick={(e) => { e.stopPropagation(); handleToggleModPublish(mod); }}
                className={`text-xs px-2 py-1 rounded ${mod.is_published ? "text-emerald-500" : "text-amber-500"}`}>
                {mod.is_published ? "Published" : "Draft"}
              </button>
              <button onClick={(e) => { e.stopPropagation(); handleDeleteModule(mod.id, mod.title); }}
                className="text-gray-300 hover:text-rose-500 text-sm">✕</button>
              <span className="text-gray-300">{expandedMod === mod.id ? "▲" : "▼"}</span>
            </div>

            {/* Expanded topics */}
            {expandedMod === mod.id && (
              <div className="mt-3 pl-8 border-l-2 border-brand-200 dark:border-brand-800 space-y-1">
                {(topics[mod.id] || []).map((t) => (
                  <Link key={t.id} to={`/studio/topic/${t.id}`}
                    className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50 dark:hover:bg-surface-700 no-underline group">
                    <span className="text-sm text-gray-700 dark:text-gray-300 group-hover:text-brand-600">
                      {t.title}
                    </span>
                    <span className={`text-xs ${t.status === "published" ? "text-emerald-500" : "text-amber-500"}`}>
                      {t.status}
                    </span>
                  </Link>
                ))}
                <Link to={`/studio/topic/new?module=${mod.id}`}
                  className="flex items-center py-2 px-3 text-sm text-brand-600 dark:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/10 rounded-lg no-underline">
                  + New Topic
                </Link>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
