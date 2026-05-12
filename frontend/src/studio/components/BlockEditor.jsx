import { useState, useRef } from "react";

const BLOCK_TYPES = [
  { value: "heading", label: "H Heading" },
  { value: "paragraph", label: "¶ Text" },
  { value: "code", label: "{ } Code" },
  { value: "callout", label: "💡 Callout" },
  { value: "assignment", label: "📝 Problem" },
  { value: "revision", label: "📌 Revision" },
  { value: "divider", label: "— Divider" },
];

export default function BlockEditor({ blocks, onChange }) {
  const [draggedIdx, setDraggedIdx] = useState(null);

  const handleDragStart = (e, index) => {
    setDraggedIdx(index);
    e.dataTransfer.effectAllowed = "move";
    // Slightly fade the element being dragged
    e.target.style.opacity = "0.5";
  };

  const handleDragEnd = (e) => {
    e.target.style.opacity = "1";
    setDraggedIdx(null);
  };

  const handleDragOver = (e, index) => {
    e.preventDefault();
    if (draggedIdx === null || draggedIdx === index) return;
    
    // Simple reorder on hover
    const newBlocks = [...blocks];
    const draggedBlock = newBlocks[draggedIdx];
    newBlocks.splice(draggedIdx, 1);
    newBlocks.splice(index, 0, draggedBlock);
    
    onChange(newBlocks);
    setDraggedIdx(index); // update index to follow the item
  };

  const updateBlock = (index, field, value) => {
    const newBlocks = [...blocks];
    newBlocks[index] = { ...newBlocks[index], [field]: value };
    onChange(newBlocks);
  };

  const updateMeta = (index, key, value) => {
    const newBlocks = [...blocks];
    newBlocks[index] = {
      ...newBlocks[index],
      meta_json: { ...(newBlocks[index].meta_json || {}), [key]: value },
    };
    onChange(newBlocks);
  };

  const addBlock = (index, type = "paragraph") => {
    const newBlocks = [...blocks];
    const newBlock = {
      id: Date.now() + Math.random(),
      block_type: type,
      content: "",
      language: type === "code" ? "c" : "",
      meta_json: type === "heading" ? { level: 2 } : type === "callout" ? { style: "tip" } : {},
    };
    newBlocks.splice(index + 1, 0, newBlock);
    onChange(newBlocks);
  };

  const deleteBlock = (index) => {
    if (blocks.length === 1) return; // don't delete last block
    const newBlocks = blocks.filter((_, i) => i !== index);
    onChange(newBlocks);
  };

  return (
    <div className="max-w-3xl mx-auto pb-32">
      {blocks.map((block, index) => (
        <div key={block.id} className="group relative mb-2">
          {/* Add block button (above) - only show for first item or let the bottom one handle it?
              Actually, let's put an add button between every block on hover. */}
          
          <div className="absolute -top-3 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 z-10 transition-opacity">
            <button
              onClick={() => addBlock(index - 1)}
              className="w-6 h-6 bg-brand-600 text-white rounded-full shadow-md flex items-center justify-center hover:scale-110 transition-transform"
              title="Add block here"
            >
              +
            </button>
          </div>

          <div
            className="flex items-start gap-2 p-2 rounded-xl border border-transparent hover:border-gray-200 dark:hover:border-gray-700 bg-white dark:bg-surface-800 transition-colors"
            draggable
            onDragStart={(e) => handleDragStart(e, index)}
            onDragEnd={handleDragEnd}
            onDragOver={(e) => handleDragOver(e, index)}
          >
            {/* Drag Handle */}
            <div className="mt-2 text-gray-300 dark:text-gray-600 cursor-grab active:cursor-grabbing hover:text-gray-500">
              ⋮⋮
            </div>

            {/* Block Type Selector */}
            <div className="w-32 flex-shrink-0">
              <select
                value={block.block_type}
                onChange={(e) => {
                  const type = e.target.value;
                  updateBlock(index, "block_type", type);
                  if (type === "heading" && !block.meta_json?.level) updateMeta(index, "level", 2);
                  if (type === "callout" && !block.meta_json?.style) updateMeta(index, "style", "tip");
                  if (type === "code" && !block.language) updateBlock(index, "language", "c");
                }}
                className="w-full text-xs font-medium bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-lg p-1.5 text-gray-700 dark:text-gray-300 outline-none"
              >
                {BLOCK_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>

            {/* Content Editor */}
            <div className="flex-1 min-w-0 flex flex-col gap-2">
              {/* Type-specific controls */}
              {block.block_type === "heading" && (
                <div className="flex gap-2">
                  {[2, 3, 4].map(lvl => (
                    <button
                      key={lvl}
                      onClick={() => updateMeta(index, "level", lvl)}
                      className={`text-xs px-2 py-1 rounded-md border ${
                        block.meta_json?.level === lvl
                          ? "bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800 dark:text-brand-300"
                          : "bg-gray-50 border-gray-200 text-gray-600 dark:bg-surface-700 dark:border-gray-600 dark:text-gray-400"
                      }`}
                    >
                      H{lvl}
                    </button>
                  ))}
                </div>
              )}

              {block.block_type === "callout" && (
                <div className="flex gap-2">
                  {["tip", "warning", "note"].map(style => (
                    <button
                      key={style}
                      onClick={() => updateMeta(index, "style", style)}
                      className={`text-xs px-2 py-1 rounded-md border capitalize ${
                        block.meta_json?.style === style
                          ? "bg-brand-50 border-brand-200 text-brand-700 dark:bg-brand-900/30 dark:border-brand-800 dark:text-brand-300"
                          : "bg-gray-50 border-gray-200 text-gray-600 dark:bg-surface-700 dark:border-gray-600 dark:text-gray-400"
                      }`}
                    >
                      {style}
                    </button>
                  ))}
                </div>
              )}

              {block.block_type === "code" && (
                <input
                  type="text"
                  placeholder="Language (e.g., c, python)"
                  value={block.language || ""}
                  onChange={(e) => updateBlock(index, "language", e.target.value)}
                  className="text-xs w-32 bg-gray-50 dark:bg-surface-700 border border-gray-200 dark:border-gray-600 rounded-lg p-1.5 outline-none text-brand-600 dark:text-brand-400 font-mono"
                />
              )}

              {/* Main Textarea */}
              {block.block_type !== "divider" && (
                <textarea
                  value={block.content || ""}
                  onChange={(e) => updateBlock(index, "content", e.target.value)}
                  placeholder={`Write ${block.block_type}... (Markdown supported)`}
                  className={`w-full bg-transparent border-none outline-none resize-none overflow-hidden ${
                    block.block_type === "heading" ? "text-xl font-bold" :
                    block.block_type === "code" ? "font-mono text-sm bg-gray-50 dark:bg-surface-900 p-3 rounded-lg border border-gray-200 dark:border-gray-700" :
                    "text-gray-700 dark:text-gray-300 leading-relaxed"
                  }`}
                  rows={block.content ? block.content.split("\\n").length : 1}
                  onInput={(e) => {
                    e.target.style.height = "auto";
                    e.target.style.height = e.target.scrollHeight + "px";
                  }}
                />
              )}
              {block.block_type === "divider" && (
                <hr className="my-4 border-gray-200 dark:border-gray-700" />
              )}
            </div>

            {/* Delete button */}
            <button
              onClick={() => deleteBlock(index)}
              className="mt-1 p-1.5 text-gray-400 hover:text-rose-500 rounded-md hover:bg-rose-50 dark:hover:bg-rose-900/20 opacity-0 group-hover:opacity-100 transition-all"
              title="Delete block"
            >
              ✕
            </button>
          </div>
          
          {/* Add block button at the very end if it's the last block */}
          {index === blocks.length - 1 && (
            <div className="absolute -bottom-3 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 z-10 transition-opacity">
              <button
                onClick={() => addBlock(index)}
                className="w-6 h-6 bg-brand-600 text-white rounded-full shadow-md flex items-center justify-center hover:scale-110 transition-transform"
                title="Add block below"
              >
                +
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
