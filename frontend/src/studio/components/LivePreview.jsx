import CodeBlock from "../../components/CodeBlock";

// Basic markdown to HTML converter for simple previews
const parseMarkdown = (text) => {
  if (!text) return "";
  let html = text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // bold
    .replace(/\*(.*?)\*/g, "<em>$1</em>") // italic
    .replace(/`(.*?)`/g, "<code>$1</code>") // inline code
    .replace(/\n/g, "<br/>"); // newlines
  return html;
};

export default function LivePreview({ blocks }) {
  if (!blocks || blocks.length === 0) {
    return (
      <div className="text-center py-20 text-gray-400">
        Start writing to see preview
      </div>
    );
  }

  return (
    <div className="prose-content pb-32">
      <div className="space-y-6">
        {blocks.map((block) => (
          <BlockRenderer key={block.id || Math.random()} block={block} />
        ))}
      </div>
    </div>
  );
}

function BlockRenderer({ block }) {
  const { block_type, content, language, meta_json } = block;

  if (!content && block_type !== "divider") return null;

  switch (block_type) {
    case "heading": {
      const level = meta_json?.level || 2;
      const Tag = `h${level}`;
      return <Tag className="text-gray-900 dark:text-white mt-8 mb-4">{content}</Tag>;
    }

    case "paragraph":
      return (
        <div 
          className="text-gray-600 dark:text-gray-300 leading-relaxed markdown-preview"
          dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
        />
      );

    case "code":
      return (
        <div className="my-4">
          <CodeBlock code={content} language={language || "c"} />
        </div>
      );

    case "callout": {
      const style = meta_json?.style || "tip";
      const colors = {
        tip: "bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200",
        warning: "bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-200",
        note: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200",
      };
      const icons = { tip: "💡", warning: "⚠️", note: "📝" };

      return (
        <div className={`my-4 p-4 border rounded-xl flex gap-3 text-sm leading-relaxed ${colors[style]}`}>
          <span className="text-lg flex-shrink-0">{icons[style]}</span>
          <div 
            className="markdown-preview"
            dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
          />
        </div>
      );
    }

    case "assignment":
      return (
        <div className="my-6 p-5 border border-brand-200 dark:border-brand-800 bg-white dark:bg-surface-800 rounded-2xl shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl">💪</span>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white m-0">Practice Problem</h3>
            {meta_json?.difficulty && (
              <span className={`text-xs px-2 py-0.5 rounded-full ml-auto ${
                meta_json.difficulty === "easy" ? "badge-easy" :
                meta_json.difficulty === "medium" ? "badge-medium" : "badge-hard"
              }`}>
                {meta_json.difficulty}
              </span>
            )}
          </div>
          <div 
            className="text-gray-600 dark:text-gray-300 text-sm markdown-preview"
            dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
          />
        </div>
      );

    case "revision":
      return (
        <div className="my-6 p-5 border border-purple-200 dark:border-purple-800/50 bg-purple-50 dark:bg-purple-900/10 rounded-2xl">
          <h4 className="text-purple-800 dark:text-purple-300 font-semibold m-0 mb-2 flex items-center gap-2">
            <span>📌</span> Key Takeaway
          </h4>
          <div 
            className="text-purple-700 dark:text-purple-200 text-sm markdown-preview"
            dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
          />
        </div>
      );

    case "divider":
      return <hr className="my-8 border-gray-200 dark:border-gray-700/50" />;

    default:
      return (
        <div className="text-rose-500 text-sm p-4 border border-rose-200 rounded">
          Unknown block type: {block_type}
        </div>
      );
  }
}
