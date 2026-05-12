/**
 * Banner ad placeholder — ready for Google AdSense integration.
 * Set `position` to "top" or "bottom" to control placement.
 *
 * Future: Replace inner div with AdSense script tag.
 */
export function BannerAd({ position = "top" }) {
  // Set to true when AdSense is integrated
  const ADS_ENABLED = false;

  if (!ADS_ENABLED) return null;

  return (
    <div
      className={`w-full flex justify-center py-2 px-4 ${
        position === "top" ? "border-b border-gray-100 dark:border-gray-800" : ""
      }`}
      data-ad-slot={`banner-${position}`}
      aria-label="Advertisement"
    >
      <div className="w-full max-w-4xl h-[90px] bg-gray-50 dark:bg-surface-700 rounded-lg flex items-center justify-center text-xs text-gray-400">
        {/* Replace this with AdSense code */}
        Ad Space — Banner {position}
      </div>
    </div>
  );
}
