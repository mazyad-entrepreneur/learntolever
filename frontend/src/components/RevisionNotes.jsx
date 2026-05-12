/**
 * Displays revision notes for a module — key points and mind-map data.
 */
export default function RevisionNotes({ notes }) {
  if (!notes || notes.length === 0) {
    return (
      <div className="content-section text-center py-12">
        <p className="text-gray-400 dark:text-gray-500">No revision notes yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {notes.map((note) => (
        <div key={note.id} className="content-section" id={`revision-${note.id}`}>
          <h3 className="text-gray-900 dark:text-white mb-3">{note.title}</h3>

          {/* Summary */}
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
            {note.summary}
          </p>

          {/* Key points */}
          {note.key_points && (
            <div className="bg-brand-50 dark:bg-brand-900/20 rounded-xl p-4 border border-brand-200 dark:border-brand-800">
              <h4 className="text-sm font-semibold text-brand-700 dark:text-brand-300 mb-2">
                Key Takeaways
              </h4>
              <ul className="space-y-1.5">
                {note.key_points.split("\n").filter(Boolean).map((point, i) => (
                  <li key={i} className="text-sm text-brand-800 dark:text-brand-200 flex items-start gap-2">
                    <span className="mt-1 w-1.5 h-1.5 rounded-full bg-brand-500 flex-shrink-0" />
                    <span>{point.replace(/^[•\-]\s*/, "")}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Mind map placeholder */}
          {note.mindmap_data && (
            <div className="mt-4 p-4 bg-gray-50 dark:bg-surface-700 rounded-xl text-sm text-gray-500 dark:text-gray-400 whitespace-pre-line">
              <h4 className="font-semibold mb-2">🗺️ Mind Map</h4>
              {note.mindmap_data}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
