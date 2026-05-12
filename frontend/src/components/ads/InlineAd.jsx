/**
 * Inline content ad placeholder — sits between content sections.
 *
 * Future: Replace inner div with AdSense code.
 */
export function InlineAd() {
  const ADS_ENABLED = false;

  if (!ADS_ENABLED) return null;

  return (
    <div
      className="my-6 flex justify-center"
      data-ad-slot="inline-content"
      aria-label="Advertisement"
    >
      <div className="w-full max-w-2xl h-[100px] bg-gray-50 dark:bg-surface-700 rounded-lg flex items-center justify-center text-xs text-gray-400">
        {/* Replace this with AdSense code */}
        Ad Space — Inline
      </div>
    </div>
  );
}
