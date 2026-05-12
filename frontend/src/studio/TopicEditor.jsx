import { useState, useEffect, useCallback } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import {
  fetchTopic, createTopic, updateTopic,
  bulkSaveBlocks, publishTopic, unpublishTopic,
} from "../api/studioApi";
import BlockEditor from "./components/BlockEditor";
import LivePreview from "./components/LivePreview";

export default function TopicEditor() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const nav = useNavigate();
  const isNew = id === "new";
  const moduleId = searchParams.get("module");

  const [title, setTitle] = useState("");
  const [status, setStatus] = useState("draft");
  const [blocks, setBlocks] = useState([]);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [showPreview, setShowPreview] = useState(true);

  useEffect(() => {
    if (!isNew && id) loadTopic();
    else setBlocks([{ id: Date.now(), block_type: "heading", content: "", language: "", meta_json: { level: 2 } }]);
  }, [id]);

  const loadTopic = async () => {
    const data = await fetchTopic(id);
    setTitle(data.title);
    setStatus(data.status);
    setBlocks(
      data.blocks?.length > 0
        ? data.blocks.map((b) => ({ ...b, id: b.id || Date.now() + Math.random() }))
        : [{ id: Date.now(), block_type: "heading", content: "", language: "", meta_json: { level: 2 } }]
    );
  };

  const handleSave = useCallback(async () => {
    setSaving(true);
    setSaved(false);
    try {
      let topicId = id;
      if (isNew) {
        if (!moduleId) { alert("Module ID required"); return; }
        const res = await createTopic({ module: parseInt(moduleId), title: title || "Untitled Topic", status: "draft" });
        topicId = res.id;
        nav(`/studio/topic/${topicId}`, { replace: true });
      } else {
        await updateTopic(id, { title });
      }
      await bulkSaveBlocks(topicId, blocks.map((b, i) => ({
        block_type: b.block_type,
        content: b.content,
        language: b.language || "",
        meta_json: b.meta_json || {},
        order: i,
      })));
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (e) {
      alert("Save failed: " + e.message);
    } finally {
      setSaving(false);
    }
  }, [id, isNew, moduleId, title, blocks, nav]);

  const handlePublish = async () => {
    if (isNew) return;
    if (status === "published") {
      await unpublishTopic(id);
      setStatus("draft");
    } else {
      await publishTopic(id);
      setStatus("published");
    }
  };

  // Keyboard shortcut: Ctrl+S to save
  useEffect(() => {
    const handler = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        handleSave();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleSave]);

  return (
    <div className="fade-in h-full flex flex-col -m-6">
      {/* Toolbar */}
      <div className="flex items-center gap-3 px-6 py-3 bg-white dark:bg-surface-800 border-b border-gray-200 dark:border-gray-700/30 flex-shrink-0">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Topic title..."
          className="flex-1 text-lg font-semibold bg-transparent text-gray-900 dark:text-white border-none outline-none placeholder-gray-300"
        />
        <button
          onClick={() => setShowPreview(!showPreview)}
          className={`px-3 py-1.5 text-xs rounded-lg border transition-all ${
            showPreview
              ? "bg-brand-50 dark:bg-brand-900/20 text-brand-600 border-brand-200 dark:border-brand-800"
              : "text-gray-400 border-gray-200 dark:border-gray-600"
          }`}
        >
          {showPreview ? "◉ Preview" : "○ Preview"}
        </button>
        <button
          onClick={handlePublish}
          disabled={isNew}
          className={`px-3 py-1.5 text-xs rounded-lg font-medium ${
            status === "published"
              ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
              : "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
          } disabled:opacity-50`}
        >
          {status === "published" ? "● Published" : "● Draft"}
        </button>
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-4 py-1.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-all disabled:opacity-50"
        >
          {saving ? "Saving..." : saved ? "✓ Saved" : "Save"}
        </button>
      </div>

      {/* Editor + Preview */}
      <div className="flex-1 flex overflow-hidden">
        {/* Editor Panel */}
        <div className={`${showPreview ? "w-1/2" : "w-full"} overflow-y-auto p-6 border-r border-gray-200 dark:border-gray-700/30`}>
          <BlockEditor blocks={blocks} onChange={setBlocks} />
        </div>

        {/* Preview Panel */}
        {showPreview && (
          <div className="w-1/2 overflow-y-auto p-6 bg-gray-50 dark:bg-surface-900">
            <div className="max-w-2xl mx-auto">
              <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-8">
                {title || "Untitled Topic"}
              </h1>
              <LivePreview blocks={blocks} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
