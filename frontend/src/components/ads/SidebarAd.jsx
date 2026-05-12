/**
 * Sidebar ad placeholder — positioned below navigation.
 *
 * Future: Replace inner div with AdSense code.
 */
export function SidebarAd() {
  const ADS_ENABLED = false;

  if (!ADS_ENABLED) return null;

  return (
    <div
      className="mt-6 p-2"
      data-ad-slot="sidebar"
      aria-label="Advertisement"
    >
      <div className="w-full h-[250px] bg-gray-50 dark:bg-surface-700 rounded-lg flex items-center justify-center text-xs text-gray-400">
        {/* Replace this with AdSense code */}
        Ad Space — Sidebar
      </div>
    </div>
  );
}
