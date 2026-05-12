import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import { BannerAd } from "./ads/BannerAd";
import { useState } from "react";
import { Outlet } from "react-router-dom";

/**
 * Main layout wrapper — navbar + sidebar + content area.
 * Responsive: sidebar collapses on mobile.
 */
export default function Layout({ darkMode, setDarkMode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
      />

      {/* Optional top banner ad slot */}
      <BannerAd position="top" />

      <div className="flex flex-1">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <main className="flex-1 min-w-0 p-4 md:p-8 lg:p-10 max-w-5xl mx-auto w-full">
          <div className="fade-in">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
