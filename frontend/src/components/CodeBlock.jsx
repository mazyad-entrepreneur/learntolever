import { useState } from "react";

/**
 * Styled code block with copy button and language label.
 */
export default function CodeBlock({ code, language = "python" }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group my-4">
      {/* Copy button */}
      <button
        onClick={handleCopy}
        className="absolute top-2 right-2 px-2.5 py-1 text-xs rounded-md
          bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white
          opacity-0 group-hover:opacity-100 transition-all duration-200"
      >
        {copied ? "✓ Copied" : "Copy"}
      </button>

      <pre className="code-block">
        <code>{code}</code>
      </pre>
    </div>
  );
}
