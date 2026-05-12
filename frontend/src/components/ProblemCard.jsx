import { useState } from "react";
import CodeBlock from "./CodeBlock";

/**
 * Expandable problem card with hints, solution, and explanation.
 */
export default function ProblemCard({ problem }) {
  const [showHints, setShowHints] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  const difficultyClass = {
    easy: "badge-easy",
    medium: "badge-medium",
    hard: "badge-hard",
  }[problem.difficulty] || "badge-easy";

  return (
    <div className="content-section" id={`problem-${problem.id}`}>
      {/* Header */}
      <div className="flex flex-wrap items-center gap-2 mb-3">
        <h4 className="text-gray-900 dark:text-white flex-1">{problem.title}</h4>
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${difficultyClass}`}>
          {problem.difficulty}
        </span>
        <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300">
          {problem.category}
        </span>
      </div>

      {/* Problem description */}
      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
        {problem.description}
      </p>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-2">
        {problem.hints && (
          <button
            onClick={() => setShowHints(!showHints)}
            className="px-3 py-1.5 text-xs font-medium rounded-lg
              bg-amber-50 text-amber-700 hover:bg-amber-100
              dark:bg-amber-900/30 dark:text-amber-300 dark:hover:bg-amber-900/50
              transition-colors"
          >
            {showHints ? "Hide Hints" : "💡 Show Hints"}
          </button>
        )}
        <button
          onClick={() => setShowSolution(!showSolution)}
          className="px-3 py-1.5 text-xs font-medium rounded-lg
            bg-brand-50 text-brand-700 hover:bg-brand-100
            dark:bg-brand-900/30 dark:text-brand-300 dark:hover:bg-brand-900/50
            transition-colors"
        >
          {showSolution ? "Hide Solution" : "🔓 Show Solution"}
        </button>
      </div>

      {/* Hints */}
      {showHints && problem.hints && (
        <div className="mt-4 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl text-sm text-amber-800 dark:text-amber-200 whitespace-pre-line">
          {problem.hints}
        </div>
      )}

      {/* Solution */}
      {showSolution && (
        <div className="mt-4 space-y-3">
          {problem.solution_code && (
            <CodeBlock code={problem.solution_code} language="python" />
          )}
          {problem.solution_explanation && (
            <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-800 dark:text-emerald-200 whitespace-pre-line">
              <strong className="block mb-1">Explanation:</strong>
              {problem.solution_explanation}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
