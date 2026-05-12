import CodeBlock from "./CodeBlock";

/**
 * Renders structured topic content sections.
 * Each section only renders if the data exists.
 */
export default function ContentRenderer({ topic }) {
  const sections = [
    {
      key: "introduction",
      title: "📖 Introduction",
      content: topic.introduction,
      type: "text",
    },
    {
      key: "content_html",
      title: "📚 Explanation",
      content: topic.content_html,
      type: "html",
    },
    {
      key: "code_examples",
      title: "💻 Code Examples",
      content: topic.code_examples,
      type: "code",
    },
    {
      key: "logic_explanation",
      title: "🧠 Logic Breakdown",
      content: topic.logic_explanation,
      type: "text",
    },
    {
      key: "common_mistakes",
      title: "⚠️ Common Mistakes",
      content: topic.common_mistakes,
      type: "warning",
    },
    {
      key: "beginner_notes",
      title: "💡 Beginner Notes",
      content: topic.beginner_notes,
      type: "tip",
    },
    {
      key: "visual_explanation",
      title: "🎨 Visual Explanation",
      content: topic.visual_explanation,
      type: "html",
    },
  ];

  return (
    <div className="space-y-6">
      {sections.map(({ key, title, content, type }) => {
        if (!content || !content.trim()) return null;

        return (
          <section key={key} className="content-section" id={`section-${key}`}>
            <h2 className="mb-4 text-gray-900 dark:text-white">{title}</h2>

            {type === "text" && (
              <div className="text-gray-600 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                {content}
              </div>
            )}

            {type === "html" && (
              <div
                className="prose-content text-gray-600 dark:text-gray-300"
                dangerouslySetInnerHTML={{ __html: content }}
              />
            )}

            {type === "code" && <CodeBlock code={content} language="python" />}

            {type === "warning" && (
              <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl p-4 text-amber-800 dark:text-amber-200 whitespace-pre-line text-sm leading-relaxed">
                {content}
              </div>
            )}

            {type === "tip" && (
              <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-4 text-emerald-800 dark:text-emerald-200 whitespace-pre-line text-sm leading-relaxed">
                {content}
              </div>
            )}
          </section>
        );
      })}

      {/* Concepts */}
      {topic.concepts && topic.concepts.length > 0 && (
        <section className="content-section" id="section-concepts">
          <h2 className="mb-4 text-gray-900 dark:text-white">🔑 Key Concepts</h2>
          <div className="space-y-5">
            {topic.concepts.map((concept) => (
              <div key={concept.id} className="pl-4 border-l-3 border-brand-400">
                <h4 className="text-gray-800 dark:text-gray-200 mb-1">{concept.title}</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  {concept.explanation}
                </p>
                {concept.code_snippet && (
                  <CodeBlock code={concept.code_snippet} language={concept.language} />
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
